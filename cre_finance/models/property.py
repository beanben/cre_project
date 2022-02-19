from django.db import models
from django.forms import ModelForm
from django.urls import reverse
import requests
import urllib
import pdb
import json


def get_coordinates(street, city, postalcode):
    query_inputs = {
        "street": street,
        "city": city,
        "postalcode": postalcode
    }
    query_params = {k: v for (k, v) in query_inputs.items() if len(v) != 0}
    query_string = urllib.parse.urlencode(query_params)
    # query_string = urllib.parse.quote_plus(address)
    geo_url = f'https://nominatim.openstreetmap.org/search.php?{query_string}&format=jsonv2'
    response = requests.get(geo_url)
    if len(response.json()) != 0:
        latitude = response.json()[0]['lat']
        longitude = response.json()[0]['lon']
        place_id = response.json()[0]['place_id']

        return latitude, longitude, place_id


def get_address(place_id):
    geo_url = f'https://nominatim.openstreetmap.org/details.php?place_id={place_id}&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json'
    response = requests.get(geo_url)
    country = response.json()["addresstags"]["country"]
    city = response.json()["localname"]
    return city, country


class Property(models.Model):
    name = models.CharField(blank=True, max_length=100)
    street_address = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=100)
    postcode = models.CharField(blank=True, max_length=100)
    country = models.CharField(blank=True, max_length=100)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)

    def clean(self):
        if self.longitude == 0 or self.latitude == 0:
            self.latitude, self.longitude, place_id = get_coordinates(
                street=self.street_address,
                city=self.city,
                postalcode=self.postcode
            )
            pdb.set_trace()
            if not self.city:
                self.city = get_address(place_id)[0]
            if not self.country:
                self.country = get_address(place_id)[1]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('property:detail', kwargs={'property_pk': self.pk})


class PropertyForm(ModelForm):
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
