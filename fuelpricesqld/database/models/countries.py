import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column

from fuelpricesqld.database.models.base import Base, UuidPkMixin


class Country(Base, UuidPkMixin):
    __tablename__ = "Countries"

    name: Mapped[str] = mapped_column(sql.NVARCHAR(16), index=True, unique=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r})"
