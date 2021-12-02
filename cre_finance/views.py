from .models.cost import Cost, CostForm, CostFormSet
from .models.building import Building, BuildingForm
from .models.loan import Loan, LoanForm, LoanUpdateForm
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
import pandas as pd


# <===== VIEWS COMBINING MODELS =====>
def home(request):
    buildings = Building.objects.all()
    loans = Loan.objects.all()

    context = {
        "buildings": buildings,
        "loans": loans
    }
    return render(request, 'cre_finance/home.html', context)


# <=====  BUILDING VIEWS =====>
class BuildingCreateView(CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'building_create.html'


class BuildingDetailView(DetailView):
    model = Building

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["building_cost"] = self.object.cost_set.all()
        return context


class BuildingListView(ListView):
    model = Building
    template_name = "home.html"


class BuildingUpdateView(UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = "update_form.html"


class BuildingDeleteView(DeleteView):
    model = Building
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('home')


# <===== COST VIEWS =====>
class CostCreateView(CreateView):
    model = Cost
    form_class = CostForm
    template_name = 'cost_create.html'

    def post(self, request, building_id, *args, **kwargs):
        building = Building.objects.get(pk=building_id)
        form = CostForm(request.POST)
        if form.is_valid():
            cost = form.save(commit=False)
            cost.building = building
            cost.save()
            return redirect('building-detail', pk=building_id)
        else:
            context = {"form": form}
            return render(request, self.template_name, context)


class MultipleCostCreateView(CreateView):
    model = Cost
    form_class = CostForm
    template_name = 'cost_create_multiple.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = CostFormSet(queryset=Cost.objects.none())
        return context

    def post(self, request, building_id, *args, **kwargs):
        building = Building.objects.get(pk=building_id)
        formset = CostFormSet(request.POST)
        if formset.is_valid():
            costs = formset.save(commit=False)
            costs.building = building
            costs.save()
            return redirect('building-detail', pk=building_id)
        else:
            print("formset.errors:", formset.errors)
            context = {"formset": formset}
            return render(request, self.template_name, context)


def create_multiple_costs(request, building_id):
    template_name = 'cost_create_multiple.html'
    building = Building.objects.get(pk=building_id)
    CostFormSet = modelformset_factory(Cost,
                                       extra=0,
                                       form=CostForm,
                                       )
    if request.method == 'POST':
        formset = CostFormSet(request.POST,
                              initial=[{"building": building}])
        if formset.is_valid():
            # do something with the formset.cleaned_data
            formset.save()
    else:
        formset = CostFormSet()
    return render(request, template_name, {'formset': formset})


class CostDetailView(DetailView):
    model = Cost


class CostDeleteView(DeleteView):
    model = Cost
    template_name = "confirm_delete.html"

    def get_success_url(self):
        return reverse('building-detail', kwargs={'pk': self.object.building.id})


class CostUpdateView(UpdateView):
    model = Cost
    form_class = CostForm
    template_name = "update_form.html"


# <===== LOAN VIEWS =====>
class LoanCreateView(CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loan_create.html'


class LoanDetailView(DetailView):
    model = Loan

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan = self.object
        development_schedule = loan.building.development_schedule
        context.update({
            "development_start": min(development_schedule.index).date,
            "development_end": max(development_schedule.index).date,
            "funding_required": development_schedule["total"].sum(),
        })

        return context


class LoanDeleteView(DeleteView):
    model = Loan
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('home')


class LoanUpdateView(UpdateView):
    model = Loan
    form_class = LoanUpdateForm
    template_name = "update_form.html"


def loan_calculate(request, pk):
    loan = Loan.objects.get(pk=pk)
    loan.calculate()
    return redirect('loan-detail', pk=pk)
