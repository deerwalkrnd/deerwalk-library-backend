from app.core.domain.repositories.repository_interface import \
    RepositoryInterface
from app.modules.feedbacks.domain.entities.feedback import Feedback


class FeedbackRepositoryInterface(RepositoryInterface[Feedback]):
    pass
