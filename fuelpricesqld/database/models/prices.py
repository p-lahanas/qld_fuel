from datetime import datetime

import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fuelpricesqld.database.models.base import Base
from fuelpricesqld.database.models.country import Country
from fuelpricesqld.database.models.fuels import Fuel
from fuelpricesqld.database.models.sites import Site


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(sql.Integer, primary_key=True, autoincrement=True)

    site_id: Mapped[int] = mapped_column(sql.ForeignKey("sites.site_id"))
    site: Mapped[Site] = relationship()

    fuel_id: Mapped[int] = mapped_column(sql.ForeignKey("fuels.fuel_id"))
    fuel: Mapped[Fuel] = relationship()

    collection_method: Mapped[str] = mapped_column(sql.CHAR)
    transaction_date_utc: Mapped[datetime] = mapped_column(sql.DateTime, index=True)

    price: Mapped[int] = mapped_column(sql.Integer)

    country_id: Mapped[int] = mapped_column(sql.ForeignKey("countries.country_id"))
    country: Mapped[Country] = relationship()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, price={self.price!r})"
