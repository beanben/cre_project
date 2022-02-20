from django.urls import path, include
from .views import (home,
                    PropertyCreateView,
                    PropertyUpdateView,
                    PropertyDeleteView,
                    SponsorCreateView,
                    SponsorUpdateView,
                    SponsorDeleteView,
                    )


property_patterns = ([
    path('create/', PropertyCreateView.as_view(), name="create"),
    path('<int:property_pk>/update/', PropertyUpdateView.as_view(), name="update"),
    path('<int:property_pk>/delete/', PropertyDeleteView.as_view(), name="delete"),
], 'property')

sponsor_patterns = ([
    path('create/', SponsorCreateView.as_view(), name="create"),
    path('<int:sponsor_pk>/update/', SponsorUpdateView.as_view(), name="update"),
    path('<int:sponsor_pk>/delete/', SponsorDeleteView.as_view(), name="delete"),
], 'sponsor')

urlpatterns = [
    path('', home, name="home"),
    path('property/', include(property_patterns)),
    path('sponsor/', include(sponsor_patterns))
]
