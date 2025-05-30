import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fuelpricesqld.database.models.base import Base
from fuelpricesqld.database.models.country import Country


class Region(Base):
    __tablename__ = "regions"

    # Composite primary key of region_level_id and region_id
    region_level_id: Mapped[int] = mapped_column(primary_key=True)
    region_id: Mapped[int] = mapped_column(primary_key=True)

    region_parent_id: Mapped[int]

    name: Mapped[str] = mapped_column(sql.VARCHAR(16))
    abbrev: Mapped[str] = mapped_column(sql.CHAR(3))

    country_id: Mapped[int] = mapped_column(sql.ForeignKey("countries.country_id"))
    country: Mapped[Country] = relationship()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(region_id={self.region_id!r}, region_level_id={self.region_level_id!r})"
