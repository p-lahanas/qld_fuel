import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column

from fuelpricesqld.database.models.base import Base


class Country(Base):
    __tablename__ = "Countries"

    country_id: Mapped[int] = mapped_column(primary_key=True)
    iso3: Mapped[str] = mapped_column(sql.CHAR(3), unique=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(country_id={self.country_id!r}, iso3={self.iso3!r})"
