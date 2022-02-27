from django.db import models
from django.forms import ModelForm
from django.urls import reverse
import requests
import urllib
import pdb
import json
from .sponsor import Sponsor


def get_ids(street, postalcode):
    query_inputs = {
        "street": street,
        "postalcode": postalcode
    }
    query_params = {k: v for (k, v) in query_inputs.items() if len(v) != 0}
    query_string = urllib.parse.urlencode(query_params)
    geo_url = f'https://nominatim.openstreetmap.org/search.php?{query_string}&format=jsonv2'
    response = requests.get(geo_url)
    if len(response.json()) != 0:
        return {
            "place_id": response.json()[0]['place_id'],
            "osm_id": response.json()[0].get('osm_id')
        }

    elif len(response.json()) == 0 and query_inputs["postalcode"]:
        return get_coordinates(street='', postalcode=postalcode)


def get_details(place_id, osm_id):
    if osm_id:
        geo_url = f'https://nominatim.openstreetmap.org/details.php?osmtype=W&osmid={osm_id}&class=highway&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json'
        response = requests.get(geo_url)
        if response.status_code == 404:
            return get_details(place_id=place_id, osm_id=False)

    elif place_id:
        geo_url = f'https://nominatim.openstreetmap.org/details.php?place_id={place_id}&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json'
        response = requests.get(geo_url)

    addresses = response.json()["address"]
    country = [el["localname"]
               for el in addresses if el["type"] == "country"][0]
    coordinates = response.json()["centroid"]["coordinates"]

    city = response.json()["localname"]
    return {
        "city": city,
        "country": country,
        "latitude": coordinates[1],
        "longitude": coordinates[0]
    }


class Building(models.Model):
    name = models.CharField(blank=True, max_length=100)
    street_address = models.CharField(blank=True, max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(blank=True, max_length=100)
    country = models.CharField(blank=True, max_length=100)
    longitude = models.FloatField(default=0, blank=True, null=True)
    latitude = models.FloatField(default=0, blank=True, null=True)
    sponsor = models.ForeignKey(
        Sponsor, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name if self.name else self.city

    def get_absolute_url(self):
        return reverse('building:detail', kwargs={'building_pk': self.pk})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        checks = [
            self.longitude == 0,
            not self.longitude,
            self.latitude == 0,
            not self.latitude,
            not self.city,
            not self.country
        ]
        if True in checks:
            ids = get_ids(
                street=self.street_address,
                postalcode=self.postcode
            )

            if ids:
                details = get_details(
                    ids["place_id"], ids["osm_id"])

                if self.longitude == 0 or not self.longitude:
                    self.longitude = details["longitude"]
                if self.latitude == 0 or not self.latitude:
                    self.latitude = details["latitude"]
                if not self.city:
                    self.city = details["city"]
                if not self.country:
                    self.country = details["country"]


class BuildingForm(ModelForm):
    prefix = 'building'

    class Meta:
        model = Building
        fields = [
            'name',
            'street_address',
            'city',
            'postcode',
            'country'
        ]


class BuildingUpdateForm(ModelForm):
    prefix = 'building'

    class Meta:
        model = Building
        fields = [
            'name',
            'street_address',
            'city',
            'postcode',
            'country',
            'latitude',
            'longitude',
        ]
