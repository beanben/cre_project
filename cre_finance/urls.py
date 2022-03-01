from django.urls import path, include
from .views import (home,
                    loan_create,
                    loan_update_description,
                    LoanDeleteView,
                    BuildingDetailView,
                    MultipleCostCreateView,
                    )


cost_patterns = ([
    path('create-multiple/', MultipleCostCreateView.as_view(),
         name="create-multiple"),
], 'cost')


building_patterns = ([
    path('<int:building_pk>/',
         BuildingDetailView.as_view(), name="detail"),
    path('<int:building_pk>/cost/', include(cost_patterns), name='cost'),
], 'building')

loan_patterns = ([
    path('create/', loan_create, name="create"),
    path('<int:loan_pk>/update_description/',
         loan_update_description, name="update_description"),
    path('<int:loan_pk>/delete/', LoanDeleteView.as_view(), name="delete"),
], 'loan')

urlpatterns = [
    path('', home, name="home"),
    path('loan/', include(loan_patterns)),
    path('building/', include(building_patterns)),
]
