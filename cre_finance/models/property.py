from django.db import models
from django.forms import ModelForm
from django.urls import reverse
import requests
import urllib
import pdb
import json
from .sponsor import Sponsor


def get_coordinates(street, city, postalcode):
    query_inputs = {
        "street": street,
        "city": city,
        "postalcode": postalcode
    }
    query_params = {k: v for (k, v) in query_inputs.items() if len(v) != 0}
    query_string = urllib.parse.urlencode(query_params)
    geo_url = f'https://nominatim.openstreetmap.org/search.php?{query_string}&format=jsonv2'
    response = requests.get(geo_url)

    if len(response.json()) != 0:
        return {
            "latitude": response.json()[0]['lat'],
            "longitude": response.json()[0]['lon'],
            "place_id": response.json()[0]['place_id'],
            "osm_id": response.json()[0].get('osm_id')
        }

    elif len(response.json()) == 0 and query_inputs["postalcode"]:
        return get_coordinates(street='', city='', postalcode=postalcode)


def get_address(place_id, osm_id):
    if osm_id:
        geo_url = f'https://nominatim.openstreetmap.org/details.php?osmtype=W&osmid={osm_id}&class=highway&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json'
        response = requests.get(geo_url)
        country = response.json()["address"][9]["localname"]

    elif place_id:
        geo_url = f'https://nominatim.openstreetmap.org/details.php?place_id={place_id}&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json'
        response = requests.get(geo_url)
        country = response.json()["address"][4]["localname"]

    city = response.json()["localname"]
    return {"city": city, "country": country}


class Property(models.Model):
    name = models.CharField(blank=True, max_length=100)
    street_address = models.CharField(blank=True, max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(blank=True, max_length=100)
    country = models.CharField(blank=True, max_length=100)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    sponsor = models.ForeignKey(
        Sponsor, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        coordinates = get_coordinates(
            street=self.street_address,
            city=self.city,
            postalcode=self.postcode
        )
        if coordinates:
            address = get_address(
                coordinates["place_id"], coordinates["osm_id"])

            if self.longitude == 0:
                self.longitude = coordinates["longitude"]
            if self.latitude == 0:
                self.latitude = coordinates["latitude"]
            if not self.city:
                self.city = address["city"]
            if not self.country:
                self.country = address["country"]

            return super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else self.city

    def get_absolute_url(self):
        return reverse('property:detail', kwargs={'property_pk': self.pk})


class PropertyForm(ModelForm):
    prefix = 'property'

    class Meta:
        model = Property
        fields = [
            'name',
            'street_address',
            'city',
            'postcode',
            'country'
        ]


class PropertyUpdateForm(ModelForm):
    prefix = 'property'

    class Meta:
        model = Property
        fields = [
            'name',
            'street_address',
            'city',
            'postcode',
            'country',
            'latitude',
            'longitude',
        ]

    # repetition of model method
    #
    # def clean(self):
    #     super().clean()
    #
    #     coordinates = get_coordinates(
    #         street=self.cleaned_data.get("street_address"),
    #         city=self.cleaned_data.get("city"),
    #         postalcode=self.cleaned_data.get("postcode")
    #     )
    #     address = get_address(coordinates["place_id"], coordinates["osm_id"])
    #
    #     if self.cleaned_data.get("longitude") == 0:
    #         self.cleaned_data["longitude"] = coordinates["longitude"]
    #
    #     if self.cleaned_data.get("latitude") == 0:
    #         self.cleaned_data["latitude"] = coordinates["latitude"]
    #
    #     if not self.cleaned_data.get("city"):
    #         self.cleaned_data["city"] = address["city"]
    #
    #     if not self.cleaned_data.get("country"):
    #         self.cleaned_data["country"] = address["country"]
