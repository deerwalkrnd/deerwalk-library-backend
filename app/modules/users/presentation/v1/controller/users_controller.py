from aiosmtplib import SMTP
from fastapi import BackgroundTasks, Depends, File, UploadFile, logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.background.tasks.email_task import send_welcome_email_task
from app.core.dependencies.database import get_db
from app.core.dependencies.get_smtp import get_smtp
from app.core.dependencies.middleware.get_current_librarian import get_current_librarian
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.domain.entities.user import User, UserWithPassword
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.infra.repositories.user_repository import UserRepository
from app.core.infra.services.email_notification_service import EmailNotificationService
from app.core.utils.make_email import create_email
from app.modules.auth.domain.templates.welcome_template import get_welcome_template
from app.modules.auth.infra.services.argon2_hasher import Argon2PasswordHasher
from app.modules.users.domain.request.user_creation_request import UserCreationRequest
from app.modules.users.domain.request.user_list_request import UserSearchRequest
from app.modules.users.domain.request.user_update_request import UpdateUserRequest
from app.modules.users.domain.response.bulk_upload_users_reponse import (
    BulkUploadUsersResponse,
)
from app.modules.users.domain.usecases.bulk_upload_users_use_case import (
    BulkUploadUsersUseCase,
)
from app.modules.users.domain.usecases.create_user_use_case import CreateUserUseCase
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
from app.modules.users.domain.usecases.update_users_by_uuid_use_case import (
    UpdateUsersByUUIDUseCase,
)


class UsersController:
    async def list_many_users(
        self,
        db: AsyncSession = Depends(get_db),
        params: UserSearchRequest = Depends(),
        _: User = Depends(get_current_librarian),
    ) -> PaginatedResponseMany[User]:
        if (
            params.searchable_field not in User.model_fields.keys()
            or not params.searchable_field
        ):
            params.searchable_field = None
            params.searchable_value = None

        user_repository = UserRepository(db=db)
        get_many_users_use_case = GetManyUsersUseCase(user_repository=user_repository)

        users = await get_many_users_use_case.execute(
            page=params.page,
            limit=params.limit,
            searchable_field=params.searchable_field,
            searchable_value=params.searchable_value,
            starts=params.starts,
            ends=params.ends,
            sort_by=params.sort_by,
            descending=params.is_descending,
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
        # _: User = Depends(get_current_librarian),
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

        argon2_hasher = Argon2PasswordHasher()

        user_creation_request.password = await argon2_hasher.hash_password(
            password=user_creation_request.password
        )

        create_user_use_case = CreateUserUseCase(user_repository=user_repository)

        try:
            new_user = await create_user_use_case.execute(
                user_creation_request=user_creation_request
            )
            send_welcome_email_task.delay(name=new_user.name, email=new_user.email)

            return new_user
        except ValueError as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500, code=ErrorCode.UNKOWN_ERROR, msg="Error Creating user"
            )

    async def delete_user(
        self,
        uuid: str,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_librarian),
    ) -> None:
        user_repository = UserRepository(db=db)

        delete_user_by_uuid_use_case = DeleteUsersByUUIDUseCase(
            user_repository=user_repository
        )
        await delete_user_by_uuid_use_case.execute(uuid)

    async def update_user(
        self,
        uuid: str,
        update_user_request: UpdateUserRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> None:
        if user.role.value != "LIBRARIAN" or user.uuid != uuid:  # type: ignore
            raise LibraryException(
                status_code=403,
                code=ErrorCode.INSUFFICIENT_PERMISSION,
                msg="You do not have permission to do this action",
            )

        user_repository = UserRepository(db=db)

        if update_user_request.password:
            pwd_service = Argon2PasswordHasher()
            update_user_request.password = await pwd_service.hash_password(
                update_user_request.password
            )

        new_data: UserWithPassword = UserWithPassword(
            **update_user_request.model_dump(exclude_unset=True)
        )

        update_users_by_uuid_use_case = UpdateUsersByUUIDUseCase(
            user_repository=user_repository
        )

        await update_users_by_uuid_use_case.execute(
            conditions=UserWithPassword(uuid=uuid), new=new_data
        )

    async def bulk_upload_users(
        self, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
    ) -> BulkUploadUsersResponse:
        if file.filename and not file.filename.endswith(".csv"):
            raise LibraryException(
                status_code=400,
                code=ErrorCode.INVALID_FIELDS,
                msg="Only CSV files are allowed!",
            )

        user_repository = UserRepository(db=db)
        bulk_upload_user_use_case = BulkUploadUsersUseCase(
            user_repository=user_repository
        )

        result = await bulk_upload_user_use_case.execute(file)
        return BulkUploadUsersResponse(
            inserted=result["inserted"], skipped=result["skipped"]
        )

    # please use this code as an example to implement your email api service
    # need to rethink and better implement this part, seperate the abstractions
    async def test_email(
        self,
        background_tasks: BackgroundTasks,
        smtp: SMTP = Depends(get_smtp),
    ):
        email_notification_service = EmailNotificationService(smtp)

        html_content = await get_welcome_template(
            name="Aashutosh Pudasaini",
        )

        email = await create_email(
            to="kesab.regmi@deerwalk.edu.np",
            subject="Welcome to Deerwalk Library",
            _from="Deerwalk Library <nepalidude3@gmail.com>",
            html=html_content,
        )

        background_tasks.add_task(email_notification_service.send_email, email)
