from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.genres.domain.entity.genre import Genre


class GenreRepositoryInterface(RepositoryInterface[Genre]):
    pass
