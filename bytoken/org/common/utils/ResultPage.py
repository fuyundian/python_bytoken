from typing import TypeVar, Generic, List, Optional
from dataclasses import dataclass, field

T = TypeVar('T')  # 泛型类型变量

@dataclass
class ResultPage(Generic[T]):
    page: int
    page_size: int
    count: int
    total_page: int
    items: Optional[List[T]] = field(default_factory=list)

    @classmethod
    def from_query(cls, items: List[T], page: int, page_size: int, total_count: int) -> "ResultPage[T]":
        """通过查询结果构造分页对象"""
        total_page = (total_count + page_size - 1) // page_size
        return cls(
            page=page,
            page_size=page_size,
            count=total_count,
            total_page=total_page,
            items=items
        )
