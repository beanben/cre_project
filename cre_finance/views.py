from .models.cost import Cost, CostForm, CostFormSet
from .models.building import Building, BuildingForm
from .models.loan import Loan, LoanForm, LoanUpdateForm
from .models.property import Property, PropertyForm, PropertyUpdateForm
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
import pandas as pd
from django.db.models import Sum


# <===== VIEWS COMBINING MODELS =====>


def home(request):
    context = {
        'properties': Property.objects.all()
    }
    return render(request, 'cre_finance/home.html', context)

# <=====  BUILDING VIEWS =====>


class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property_create.html'
    success_url = reverse_lazy('home')


class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyUpdateForm
    pk_url_kwarg = "property_pk"
    template_name = "property_update.html"
    # context_object_name = "property_selected"

    def get_success_url(self):
        return reverse('property:update', args={self.object.pk})


class PropertyDeleteView(DeleteView):
    model = Property
    pk_url_kwarg = "property_pk"
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('home')


# <=====  BUILDING VIEWS =====>


class BuildingCreateView(CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'building_create.html'


class BuildingDetailView(DetailView):
    model = Building
    pk_url_kwarg = "building_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        building_cost = self.object.cost_set.all()
        context.update({
            "building_cost": building_cost,
            "costs": building_cost.values('type').annotate(total_amount=Sum('amount'))
        })
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

    def post(self, request, building_pk, *args, **kwargs):
        building = Building.objects.get(pk=building_pk)
        form = CostForm(request.POST)
        if form.is_valid():
            cost = form.save(commit=False)
            cost.building = building
            cost.save()
            return redirect('building:detail', pk=building_pk)
        else:
            context = {"form": form}
            return render(request, self.template_name, context)


def cost_extra(request):
    nb_extras = request.POST.get('extra')
    building_pk = request.POST.get('building_pk')
    return redirect('building:cost:create-multiple', nb_extras=nb_extras, building_pk=building_pk)


class MultipleCostCreateView(CreateView):
    model = Cost
    form_class = CostForm
    template_name = 'cost_create_multiple.html'

    def get(self, request, *args, **kwargs):
        formset = CostFormSet(queryset=Cost.objects.none())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, building_pk, *args, **kwargs):
        building = Building.objects.get(pk=building_pk)
        formset = CostFormSet(data=request.POST)
        if formset.is_valid():
            costs = formset.save(commit=False)
            for cost in costs:
                cost.building = building
                cost.save()
            return redirect('building:detail', building_pk=building_pk)

        context = {"formset": formset}
        return render(request, self.template_name, context)


class MultipleCostDeleteView(DeleteView):
    model = Cost

    def post(self, request, building_pk, *args, **kwargs):
        costs = self.request.POST.getlist('cost')
        Cost.objects.filter(pk__in=costs).delete()
        return redirect('building:detail', building_pk=building_pk)


def create_multiple_costs(request, building_id):
    template_name = 'cost_create_multiple.html'
    building = Building.objects.get(pk=building_pk)
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
    pk_url_kwarg = "cost_pk"


class CostListView(ListView):
    model = Cost


class CostDeleteView(DeleteView):
    model = Cost
    template_name = "confirm_delete.html"

    def get_success_url(self):
        return reverse('building:detail', kwargs={'pk': self.object.building.pk})


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
    pk_url_kwarg = "loan_pk"

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
    pk_url_kwarg = "loan_pk"
    form_class = LoanUpdateForm
    template_name = "update_form.html"


def loan_calculate(request, loan_pk):
    loan = Loan.objects.get(pk=loan_pk)
    loan.calculate()
    return redirect('loan:detail', loan_pk=loan_pk)
