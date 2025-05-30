from datetime import datetime

import sqlalchemy as sql
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fuelpricesqld.database.models.base import Base
from fuelpricesqld.database.models.brand import Brand
from fuelpricesqld.database.models.country import Country


class Site(Base):
    __tablename__ = "sites"

    site_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sql.VARCHAR(50))
    address: Mapped[str] = mapped_column(sql.VARCHAR(50))
    postcode: Mapped[str] = mapped_column(sql.VARCHAR(16))

    g1: Mapped[str] = mapped_column(sql.VARCHAR(16))
    g2: Mapped[str] = mapped_column(sql.VARCHAR(16))
    g3: Mapped[str] = mapped_column(sql.VARCHAR(16))
    g4: Mapped[str] = mapped_column(sql.VARCHAR(16))
    g5: Mapped[str] = mapped_column(sql.VARCHAR(16))

    geo_location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="Point", srid=4326, spatial_index=True)
    )

    last_modified: Mapped[datetime] = mapped_column(sql.DateTime)

    # Shouldn't be longer than 27 chars
    google_place_id: Mapped[str] = mapped_column(sql.VARCHAR(27), unique=True)

    brand_id: Mapped[int] = mapped_column(sql.ForeignKey("brands.brand_id"))
    brand: Mapped[Brand] = relationship()

    country_id: Mapped[int] = mapped_column(sql.ForeignKey("countries.country_id"))
    country: Mapped[Country] = relationship()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(site_id={self.site_id!r}, name={self.name!r})"
        )
