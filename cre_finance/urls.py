from django.urls import path, include
from .views import (home,
                    PropertyCreateView,
                    PropertyUpdateView,
                    PropertyDeleteView
                    )


property_patterns = ([
    path('create/', PropertyCreateView.as_view(), name="create"),
    path('<int:property_pk>/update/', PropertyUpdateView.as_view(), name="update"),
    path('<int:property_pk>/delete/', PropertyDeleteView.as_view(), name="delete"),
], 'property')

urlpatterns = [
    path('', home, name="home"),
    path('property/', include(property_patterns))
]
