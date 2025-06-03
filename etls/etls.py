import logging
import os

import polars as pl
from sqlalchemy.orm import Session

import fuelpricesqld.api as fa

# from etls.lib import get_api_token
from fuelpricesqld.database.models import Brand, Fuel, Region, Site
from fuelpricesqld.database.models.prices import Price
from fuelpricesqld.database.session import make_db_engine
from fuelpricesqld.settings import Settings

logger = logging.getLogger(__name__)


def postgres_upsert(table, conn, keys, data_iter):
    from sqlalchemy.dialects.postgresql import insert

    data = [dict(zip(keys, row)) for row in data_iter]

    insert_statement = insert(table.table).values(data)
    upsert_statement = insert_statement.on_conflict_do_update(
        constraint=f"{table.table.name}_pkey",
        set_={c.key: c for c in insert_statement.excluded},
    )
    conn.execute(upsert_statement)


def etl_brands(session: Session, api_client: fa.Client):
    # Extract from API
    lf_brands = api_client.get_country_brands_lf(fa.COUNTRY_ID_AUS)

    # Transform column headings & add country_id
    lf_brands = lf_brands.rename({"BrandId": "brand_id", "Name": "name"})
    lf_brands = lf_brands.with_columns(pl.lit(fa.COUNTRY_ID_AUS).alias("country_id"))

    # Load into the DB
    lf_brands.collect().to_pandas(use_pyarrow_extension_array=True).to_sql(
        name=Brand.__tablename__,
        con=session.connection(),
        if_exists="append",
        index=False,
        method=postgres_upsert,
    )


def etl_fuels(session: Session, api_client: fa.Client):
    # Extract from API
    lf_fuels = api_client.get_fuel_types_lf(fa.COUNTRY_ID_AUS)

    # Transform column headings & add country_id
    lf_fuels = lf_fuels.rename({"FuelId": "fuel_id", "Name": "name"})
    lf_fuels = lf_fuels.with_columns(pl.lit(fa.COUNTRY_ID_AUS).alias("country_id"))

    # Load into the DB
    lf_fuels.collect().to_pandas(use_pyarrow_extension_array=True).to_sql(
        name=Fuel.__tablename__,
        con=session.connection(),
        if_exists="append",
        index=False,
        method=postgres_upsert,
    )


def etl_regions(session: Session, api_client: fa.Client):
    # Extract from API
    lf_regions = api_client.get_country_geographic_regions_lf(fa.COUNTRY_ID_AUS)

    # Transform column headings & add country_id
    lf_regions = lf_regions.rename(
        {
            "GeoRegionLevel": "region_level_id",
            "GeoRegionId": "region_id",
            "Name": "name",
            "Abbrev": "abbrev",
            "GeoRegionParentId": "region_parent_id",
        }
    )
    lf_regions = lf_regions.with_columns(pl.lit(fa.COUNTRY_ID_AUS).alias("country_id"))

    # Load into the DB
    lf_regions.collect().to_pandas(use_pyarrow_extension_array=True).to_sql(
        name=Region.__tablename__,
        con=session.connection(),
        if_exists="append",
        index=False,
        method=postgres_upsert,
    )


def etl_sites(session: Session, api_client: fa.Client):
    # Extract from API

    lf_sites = api_client.get_full_site_details_lf(
        fa.COUNTRY_ID_AUS, fa.REGION_LEVEL_BNE, fa.REGION_ID_BNE
    )

    # Transform column headings & add column_id
    lf_sites = lf_sites.drop(
        [
            "MO",
            "MC",
            "TO",
            "TC",
            "WO",
            "WC",
            "THO",
            "THC",
            "FO",
            "FC",
            "SO",
            "SC",
            "SUO",
            "SUC",
        ]
    )
    lf_sites = lf_sites.rename(
        {
            "S": "site_id",
            "A": "address",
            "N": "name",
            "B": "brand_id",
            "P": "postcode",
            "G1": "g1",
            "G2": "g2",
            "G3": "g3",
            "G4": "g4",
            "G5": "g5",
            "M": "last_modified",
            "GPI": "google_place_id",
        }
    )
    # Add geo_location as a string "POINT(lon lat)" (WKT format)
    lf_sites = lf_sites.with_columns(
        pl.format("POINT({} {})", pl.col("Lng"), pl.col("Lat")).alias("geo_location"),
        pl.col("last_modified").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.3f"),
    )
    lf_sites = lf_sites.drop(["Lng", "Lat"])
    lf_sites = lf_sites.with_columns(pl.lit(fa.COUNTRY_ID_AUS).alias("country_id"))

    # Load it into the db
    lf_sites.collect().to_pandas(use_pyarrow_extension_array=True).to_sql(
        name=Site.__tablename__,
        con=session.connection(),
        if_exists="append",
        index=False,
        method=postgres_upsert,
    )


def etl_prices(session: Session, api_client: fa.Client):
    lf_prices = api_client.get_sites_prices_lf(
        fa.COUNTRY_ID_AUS, fa.REGION_LEVEL_BNE, fa.REGION_ID_BNE
    )

    # Transform column headings & add country_id
    lf_prices = lf_prices.rename(
        {
            "SiteId": "site_id",
            "FuelId": "fuel_id",
            "CollectionMethod": "collection_method",
            "TransactionDateUtc": "transaction_date_utc",
            "Price": "price",
        }
    )
    lf_prices = lf_prices.with_columns(pl.lit(fa.COUNTRY_ID_AUS).alias("country_id"))
    lf_prices.collect().to_pandas(use_pyarrow_extension_array=True).to_sql(
        name=Price.__tablename__,
        con=session.connection(),
        if_exists="append",
        index=False,
        method=postgres_upsert,
    )


def etl(session: Session):
    # TODO: SWITCH OUT for AWS api token retrieval
    api_client = fa.Client(os.environ.get("QLDTOKEN", ""))

    # Order of these does matter due to foreign key constraints
    # Put sites after brand & ensure countries table is seeded
    etl_brands(session, api_client)
    etl_fuels(session, api_client)
    etl_regions(session, api_client)
    etl_sites(session, api_client)

    # Do prices last after we have the latest reference data
    etl_prices(session, api_client)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
    )

    settings = Settings()  # type: ignore

    engine = make_db_engine(settings.PSQL_DB_CONNECTION_STRING)

    with Session(engine) as session:
        etl(session)
        session.commit()
