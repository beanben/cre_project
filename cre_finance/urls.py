from django.urls import path
from .views import (home,
                    BuildingCreateView,
                    BuildingDetailView,
                    BuildingListView,
                    BuildingUpdateView,
                    BuildingDeleteView,
                    MultipleCostCreateView,
                    CostCreateView,
                    CostDetailView,
                    CostDeleteView,
                    CostUpdateView,
                    LoanCreateView,
                    LoanDetailView,
                    LoanDeleteView,
                    LoanUpdateView,
                    loan_calculate)

urlpatterns = [
    path('', home, name="home"),

    # <==== Building Views ====>
    path('building-create/', BuildingCreateView.as_view(), name="building-create"),
    path('building/<int:pk>/',
         BuildingDetailView.as_view(), name="building-detail"),
    path('building-update/<int:pk>/',
         BuildingUpdateView.as_view(), name="building-update"),
    path('building-delete/<int:pk>/',
         BuildingDeleteView.as_view(), name="building-delete"),

    # <==== Cost Views ====>
    path('building/<int:building_id>/cost-create/',
         CostCreateView.as_view(), name="cost-create"),
    path('building/<int:building_id>/cost-create-multiple/', MultipleCostCreateView.as_view(),
         name="cost-create-multiple"),
    path('building/<int:building_id>/cost/<int:pk>/',
         CostDetailView.as_view(), name="cost-detail"),
    path('building/<int:building_id>/cost-delete/<int:pk>/',
         CostDeleteView.as_view(), name="cost-delete"),
    path('building/<int:building_id>/cost-update/<int:pk>/',
         CostUpdateView.as_view(), name="cost-update"),

    # <==== Loan Views ====>
    path('loan-create/', LoanCreateView.as_view(), name="loan-create"),
    path('loan_calculate/<int:pk>/', loan_calculate, name="loan_calculate"),
    path('loan/<int:pk>/',
         LoanDetailView.as_view(), name="loan-detail"),
    path('loan-delete/<int:pk>/',
         LoanDeleteView.as_view(), name="loan-delete"),
    path('loan-update/<int:pk>/',
         LoanUpdateView.as_view(), name="loan-update")
]
