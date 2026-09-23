from typing import List

from pydantic import BaseModel


class PaginatedResponseMany[T](BaseModel):
    page: int
    limit: int
    total: int
    next: int | None
    items: List[T]

    @classmethod
    def build(
        cls, page: int, limit: int, total: int, items: List[T]
    ) -> "PaginatedResponseMany[T]":
        """Assemble a page from the real matching-row ``total``.

        ``next`` is None on the last page, so clients can tell they have
        reached the end instead of paging forever into empty results.
        """
        has_next = page * limit < total
        return cls(
            page=page,
            limit=limit,
            total=total,
            next=page + 1 if has_next else None,
            items=items,
        )
