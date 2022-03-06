from django.urls import path, include
from .views import (home,
                    loan_create,
                    loan_update_description,
                    LoanDeleteView,
                    BuildingDetailView,
                    MultipleCostCreateView,
                    BuildingCostUpdateView,
                    CostDeleteView
                    )


cost_patterns = ([
    path('create/', MultipleCostCreateView.as_view(), name="create"),
    path('update/', BuildingCostUpdateView.as_view(), name="update"),
    path('<int:cost_pk>/delete/', CostDeleteView.as_view(), name="delete"),
], 'cost')

building_patterns = ([
    path('<int:building_pk>/', BuildingDetailView.as_view(), name="detail"),
    path('<int:building_pk>/cost/', include(cost_patterns)),
], 'building')

loan_patterns = ([
    path('create/', loan_create, name="create"),
    path('<int:loan_pk>/update_description/',
         loan_update_description, name="update_description"),
    path('<int:loan_pk>/delete/', LoanDeleteView.as_view(), name="delete"),
    # path('<int:loan_pk>/building/', include(building_patterns)),
], 'loan')

urlpatterns = [
    path('', home, name="home"),
    path('loan/', include(loan_patterns)),
    path('building/', include(building_patterns))
]
