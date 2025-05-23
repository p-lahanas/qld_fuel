from typing import Any, Dict, Optional

import requests


class FuelApi:

    base_url = "https://fppdirectapi-prod.fuelpricesqld.com.au"

    def __init__(self, token: str):
        self._token = token

        self._headers = {"Authorization": f"FPDAPI SubscriberToken={self._token}",
                         "Content-Type": "application/json"}

        self._session = requests.Session()

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self._session.get(
            url=url, headers=self._headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_country_brands(self, country_id: int) -> dict:
        """Get all fuel brands for the specified country."""
        return self._get("/Subscriber/GetCountryBrands", {"countryId": country_id})

    def get_country_geographic_regions(self, country_id: int) -> dict:
        """List of geographic region IDs along with levels, names, abbreviations and geographic region parent ids"""
        return self._get("/Subscriber/GetCountryGeographicRegions", {"countryId": country_id})

    def get_fuel_types(self, country_id: int) -> dict:
        """ A list of fuel type IDs and names"""
        return self._get("/Subscriber/GetCountryFuelTypes", {"countryId": country_id})

    def get_full_site_details(self, country_id: int, geo_region_level: int, geo_region_id: int) -> dict:
        """Get additional site details"""
        return self._get("/Subscriber/GetFullSiteDetails", {"countryId": country_id, "geoRegionLevel": geo_region_level, "geoRegionId": geo_region_id})

    def get_sites_price(self, country_id: int, geo_region_level: int, geo_region_id: int) -> dict:
        """A list of site IDs along with fuel ids and prices."""
        return self._get("/Price/GetSitesPrices", {"countryId": country_id, "geoRegionLevel": geo_region_level, "geoRegionId": geo_region_id})
