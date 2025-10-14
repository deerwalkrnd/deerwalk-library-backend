from typing import Optional

from app.modules.quotes.domain.request.quote_create_request import QuoteCreateRequest


class QuoteResponse(QuoteCreateRequest):
    id: Optional[int]
