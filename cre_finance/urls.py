from django.urls import path, include
from .views import (home,
                    BuildingCreateView,
                    BuildingDetailView,
                    BuildingListView,
                    BuildingUpdateView,
                    BuildingDeleteView,
                    MultipleCostCreateView,
                    MultipleCostDeleteView,
                    CostCreateView,
                    CostDetailView,
                    CostListView,
                    CostDeleteView,
                    CostUpdateView,
                    LoanCreateView,
                    LoanDetailView,
                    LoanDeleteView,
                    LoanUpdateView,
                    loan_calculate)

# urlpatterns = [
#     path('', home, name="home"),
#
#     # <==== Building Views ====>
#     path('building-create/', BuildingCreateView.as_view(), name="building-create"),
#     path('building/<int:pk>/',
#          BuildingDetailView.as_view(), name="building-detail"),
#     path('building-update/<int:pk>/',
#          BuildingUpdateView.as_view(), name="building-update"),
#     path('building-delete/<int:pk>/',
#          BuildingDeleteView.as_view(), name="building-delete"),
#
#     # <==== Cost Views ====>
#     path('building/<int:building_id>/cost-create/',
#          CostCreateView.as_view(), name="cost-create"),
#     path('building/<int:building_id>/cost-create-multiple/', MultipleCostCreateView.as_view(),
#          name="cost-create-multiple"),
#     path('building/<int:building_id>/cost-list/',
#          CostListView.as_view(), name="cost-list"),
#     path('building/<int:building_id>/cost/<int:pk>/',
#          CostDetailView.as_view(), name="cost-detail"),
#     path('building/<int:building_id>/cost-delete/<int:pk>/',
#          CostDeleteView.as_view(), name="cost-delete"),
#     path('building/<int:building_id>/cost-update/<int:pk>/',
#          CostUpdateView.as_view(), name="cost-update"),
#
#     # <==== Loan Views ====>
#     path('loan-create/', LoanCreateView.as_view(), name="loan-create"),
#     path('loan_calculate/<int:pk>/', loan_calculate, name="loan_calculate"),
#     path('loan/<int:pk>/',
#          LoanDetailView.as_view(), name="loan-detail"),
#     path('loan-delete/<int:pk>/',
#          LoanDeleteView.as_view(), name="loan-delete"),
#     path('loan-update/<int:pk>/',
#          LoanUpdateView.as_view(), name="loan-update")
# ]

loan_patterns = ([
    path('create/', LoanCreateView.as_view(), name="create"),
    path('<int:loan_pk>/calculate/', loan_calculate, name="calculate"),
    path('<int:loan_pk>/', LoanDetailView.as_view(), name="detail"),
    path('<int:loan_pk>/delete/', LoanDeleteView.as_view(), name="delete"),
    path('<int:loan_pk>/loan-update/', LoanUpdateView.as_view(), name="update")
], 'loan')

building_cost_patterns = ([
    path('', CostListView.as_view(), name="list"),
    path('create/', CostCreateView.as_view(), name="create"),
    path('create-multiple/', MultipleCostCreateView.as_view(),
         name="create-multiple"),
    path('delete-multiple/', MultipleCostDeleteView.as_view(),
         name="delete-multiple"),
    path('<int:cost_pk>/cost/', CostDetailView.as_view(), name="detail"),
    path('<int:cost_pk>/delete/', CostDeleteView.as_view(), name="delete"),
    path('<int:cost_pk>/update/', CostUpdateView.as_view(), name="update"),
], 'cost')

building_patterns = ([
    path('create/', BuildingCreateView.as_view(), name="create"),
    path('<int:building_pk>/', BuildingDetailView.as_view(), name="detail"),
    path('<int:building_pk>/update/', BuildingUpdateView.as_view(), name="update"),
    path('<int:building_pk>/delete/', BuildingDeleteView.as_view(), name="delete"),
    path('<int:building_pk>/cost/', include(building_cost_patterns), name='cost'),
], 'building')

urlpatterns = [
    path('', home, name="home"),
    path('building/', include(building_patterns)),
    path('loan/', include(loan_patterns)),
]
