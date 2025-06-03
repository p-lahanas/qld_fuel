from typing import Any, Dict, Optional, Type

import polars as pl
import requests

BRANDS_SCHEMA: dict[str, Type] = {
    "BrandId": pl.Int32,
    "Name": pl.String,
}

REGIONS_SCHEMA: dict[str, Type] = {
    "GeoRegionLevel": pl.Int32,
    "GeoRegionId": pl.Int32,
    "Name": pl.String,
    "Abbrev": pl.String,
    "GeoRegionParentId": pl.Int32,
}

FUELS_SCHEMA: dict[str, Type] = {"FuelId": pl.Int32, "Name": pl.String}

SITE_SCHEMA: dict[str, Type] = {
    "S": pl.Int32,
    "A": pl.String,
    "N": pl.String,
    "B": pl.Int32,
    "P": pl.String,
    "G1": pl.Int32,
    "G2": pl.Int32,
    "G3": pl.Int32,
    "G4": pl.Int32,
    "G5": pl.Int32,
    "Lat": pl.Float32,
    "Lng": pl.Float32,
    "M": pl.String,  # manually cast this later
    "GPI": pl.String,
    "MO": pl.String,
    "MC": pl.String,
    "TO": pl.String,
    "TC": pl.String,
    "WO": pl.String,
    "WC": pl.String,
    "THO": pl.String,
    "THC": pl.String,
    "FO": pl.String,
    "FC": pl.String,
    "SO": pl.String,
    "SC": pl.String,
    "SUO": pl.String,
    "SUC": pl.String,
}

PRICE_SCHEMA: dict[str, Type] = {
    "SiteId": pl.Int32,
    "FuelId": pl.Int32,
    "CollectionMethod": pl.String,
    "TransactionDateUtc": pl.String,
    "Price": pl.Int32,
}


class Client:
    base_url = "https://fppdirectapi-prod.fuelpricesqld.com.au"

    def __init__(self, token: str):
        self._token = token

        self._headers = {
            "Authorization": f"FPDAPI SubscriberToken={self._token}",
            "Content-Type": "application/json",
        }

        self._session = requests.Session()

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self._session.get(url=url, headers=self._headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_country_brands(self, country_id: int) -> dict:
        """Get all fuel brands for the specified country."""
        return self._get("/Subscriber/GetCountryBrands", {"countryId": country_id})

    def get_country_brands_lf(self, country_id: int) -> pl.LazyFrame:
        return pl.LazyFrame(
            self.get_country_brands(country_id)["Brands"], schema=BRANDS_SCHEMA
        )

    def get_country_geographic_regions(self, country_id: int) -> dict:
        """List of geographic region IDs along with levels, names, abbreviations and geographic region parent ids"""
        return self._get(
            "/Subscriber/GetCountryGeographicRegions", {"countryId": country_id}
        )

    def get_country_geographic_regions_lf(self, country_id: int) -> pl.LazyFrame:
        return pl.LazyFrame(
            self.get_country_geographic_regions(country_id)["GeographicRegions"],
            schema=REGIONS_SCHEMA,
        )

    def get_fuel_types(self, country_id: int) -> dict:
        """A list of fuel type IDs and names"""
        return self._get("/Subscriber/GetCountryFuelTypes", {"countryId": country_id})

    def get_fuel_types_lf(self, country_id: int) -> pl.LazyFrame:
        return pl.LazyFrame(
            self.get_fuel_types(country_id)["Fuels"], schema=FUELS_SCHEMA
        )

    def get_full_site_details(
        self, country_id: int, geo_region_level: int, geo_region_id: int
    ) -> dict:
        """Get additional site details"""
        return self._get(
            "/Subscriber/GetFullSiteDetails",
            {
                "countryId": country_id,
                "geoRegionLevel": geo_region_level,
                "geoRegionId": geo_region_id,
            },
        )

    def get_full_site_details_lf(
        self, country_id: int, geo_region_level: int, geo_region_id: int
    ) -> pl.LazyFrame:
        return pl.LazyFrame(
            self.get_full_site_details(country_id, geo_region_level, geo_region_id)[
                "S"
            ],
            schema=SITE_SCHEMA,
        )

    def get_sites_prices(
        self, country_id: int, geo_region_level: int, geo_region_id: int
    ) -> dict:
        """A list of site IDs along with fuel ids and prices."""
        return self._get(
            "/Price/GetSitesPrices",
            {
                "countryId": country_id,
                "geoRegionLevel": geo_region_level,
                "geoRegionId": geo_region_id,
            },
        )

    def get_sites_prices_lf(
        self, country_id: int, geo_region_level: int, geo_region_id: int
    ) -> pl.LazyFrame:
        return pl.LazyFrame(
            self.get_sites_prices(country_id, geo_region_level, geo_region_id)[
                "SitePrices"
            ],
            schema=PRICE_SCHEMA,
        )
