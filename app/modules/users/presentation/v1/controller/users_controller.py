from typing import Union
from fastapi import Depends, File, Form, UploadFile, logger
from starlette.datastructures import UploadFile as StarletteUploadFile
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.domain.entities.user import User, UserWithPassword
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.infra.repositories.user_repository import UserRepository
from app.core.infra.services.s3_file_service import S3FileService
from app.core.models.users import UserRole
from app.modules.users.domain.request.user_creation_request import UserCreationRequest
from app.modules.users.domain.request.user_list_request import UserSearchRequest
from app.modules.users.domain.usecases.create_user_use_case import CreateUserUseCase
from aiobotocore.session import AioSession
from app.modules.users.domain.usecases.delete_users_by_uuid_use_case import (
    DeleteUsersByUUIDUseCase,
)
from app.modules.users.domain.usecases.get_many_users_use_case import (
    GetManyUsersUseCase,
)
from app.modules.users.domain.usecases.get_user_by_email_use_case import (
    GetUserByEmailUseCase,
)
from app.modules.users.domain.usecases.get_user_by_uuid_use_case import (
    GetUserByUUIDUseCase,
)


class UsersController:
    async def list_many_users(
        self, db: AsyncSession = Depends(get_db), params: UserSearchRequest = Depends()
    ) -> PaginatedResponseMany[User]:
        # TODO(aashutosh): make the searchable field part of the request and verify that
        # searchable exists on the users table.
        searchable_field = "name"
        user_repository = UserRepository(db=db)
        get_many_users_use_case = GetManyUsersUseCase(user_repository=user_repository)

        users = await get_many_users_use_case.execute(
            page=params.page,
            limit=params.limit,
            searchable_field=searchable_field if params.searchable else None,
            searchable_value=params.searchable,
            starts=params.starts,
            ends=params.ends,
        )

        return PaginatedResponseMany(
            page=params.page, total=len(users), next=params.page + 1, items=users
        )

    async def list_one_user(
        self, uuid: str, db: AsyncSession = Depends(get_db)
    ) -> User:
        user_repository = UserRepository(db=db)
        get_user_by_uuid_use_case = GetUserByUUIDUseCase(
            user_repository=user_repository
        )

        try:
            user = await get_user_by_uuid_use_case.execute(uuid=uuid)
            return user
        except ValueError:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="User with the provided UUID is not found",
                fields=["uuid"],
            )

    # add librarian only filter!
    async def create_user(
        self,
        user_creation_request: UserCreationRequest,
        db: AsyncSession = Depends(get_db),
    ) -> User:
        user_repository = UserRepository(db=db)

        get_user_by_email_use_case = GetUserByEmailUseCase(
            user_repository=user_repository
        )

        try:
            user = await get_user_by_email_use_case.execute(
                email=user_creation_request.email
            )

            if user:
                raise LibraryException(
                    status_code=409,
                    code=ErrorCode.DUPLICATE_ENTRY,
                    msg="User with that email already exists",
                )
        except ValueError:
            # this is the success path here
            pass

        create_user_use_case = CreateUserUseCase(user_repository=user_repository)

        try:
            new_user = await create_user_use_case.execute(
                user_creation_request=user_creation_request
            )
            return new_user
        except ValueError as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500, code=ErrorCode.UNKOWN_ERROR, msg="Error Creating user"
            )

    async def delete_user(self, uuid: str, db: AsyncSession = Depends(get_db)) -> None:
        user_repository = UserRepository(db=db)

        delete_user_by_uuid_use_case = DeleteUsersByUUIDUseCase(
            user_repository=user_repository
        )
        await delete_user_by_uuid_use_case.execute(uuid)

    # have to do it without pydantic here cuz multipart-form is a not mature in fastapi.
    # something to look at in the future.
    async def update_user(
        self,
        uuid: str,
        name: str | None = Form(None),
        roll_number: str | None = Form(None),
        email: EmailStr | None = Form(None),
        password: str | None = Form(None),
        graduating_year: str | None = Form(None),
        role: UserRole | None = Form(None),
        user_image: Union[UploadFile, str, None] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> None:
        user_repository = UserRepository(db=db)

        new_data = UserWithPassword(
            name=name,
            roll_number=roll_number,
            email=email,
            password=password,
            graduating_year=graduating_year,
            role=role,
        )

        # file upload is still not mature in fastapi man.
        # using this hack for now
        if isinstance(user_image, StarletteUploadFile) and user_image.filename:
            session = AioSession()
            file_service = S3FileService(session=session)
            uploaded_url = await file_service.save(
                f"profile-images/{user_image.filename}",
                await user_image.read(),
                user_image.content_type,
            )
            new_data.image_url = uploaded_url

        await user_repository.update(
            conditions=UserWithPassword(uuid=uuid), obj=new_data
        )

        return

