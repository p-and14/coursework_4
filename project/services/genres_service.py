from typing import Optional, List

from project.dao.main import GenresDAO
from project.exceptions import ItemNotFound
from project.models import Genre


class GenresService:
    def __init__(self, dao: GenresDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Genre:
        if genre := self.dao.get_by_id(pk):
            return genre
        raise ItemNotFound(f'Genre with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> List[Genre]:
        return self.dao.get_all(page=page)
