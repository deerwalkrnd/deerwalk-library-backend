from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.quotes.domain.entities.quote import Quote


class QuoteRepositoryInterface(RepositoryInterface[Quote]):
    pass
