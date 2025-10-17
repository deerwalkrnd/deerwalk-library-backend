from typing import Optional

from app.modules.quotes.domain.requests.quote_create_request import QuoteCreateRequest


class QuoteResponse(QuoteCreateRequest):
    id: Optional[int]
