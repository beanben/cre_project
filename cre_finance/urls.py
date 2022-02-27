from django.urls import path, include
from .views import (home,
                    loan_create,
                    loan_update_description,
                    LoanDeleteView,
                    MultipleCostCreateView,
                    )

building_costs_pattern = ([
    path('create/', MultipleCostCreateView.as_view(), name="create"),
], 'building_costs')

loan_patterns = ([
    path('create/', loan_create, name="create"),
    path('<int:loan_pk>/update_description/',
         loan_update_description, name="update_description"),
    path('<int:loan_pk>/delete/', LoanDeleteView.as_view(), name="delete"),
    path('<int:loan_pk>/building_costs/', include(building_costs_pattern)),
], 'loan')

urlpatterns = [
    path('', home, name="home"),
    path('loan/', include(loan_patterns)),
]
