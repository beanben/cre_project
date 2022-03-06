from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .models.building import Building, BuildingForm, BuildingUpdateForm
from .models.sponsor import Sponsor, SponsorForm
from .models.loan import Loan
from .models.broker import Broker, BrokerForm
from .models.cost import Cost, CostForm, MyCostFormSet, MyCostUpdateFormSet
from django.db.models import Sum, Count
import pdb
from pprint import pprint


def home(request):
    # building_costs = Building.objects.annotate(cost_amounts=Sum('cost__amount'))
    loan_costs_funded = Loan.objects.annotate(
        sum_costs=Sum('building__cost__amount'))
    context = {
        'loans': Loan.objects.all(),
        "loan_costs_funded": loan_costs_funded
    }
    return render(request, 'cre_finance/home.html', context)


# <=====  LOAN VIEWS =====>


def loan_create(request):
    template = 'loan_create.html'
    if request.method == 'POST':
        building_form = BuildingForm(request.POST)
        sponsor_form = SponsorForm(request.POST)
        broker_form = BrokerForm(request.POST)
        if building_form.is_valid() and sponsor_form.is_valid() and broker_form.is_valid():
            building_instance = building_form.save()
            sponsor_instance = sponsor_form.save()
            broker_instance = broker_form.save()
            loan = Loan.objects.create(
                sponsor=sponsor_instance,
                building=building_instance,
                broker=broker_instance
            )
            return redirect(
                reverse(
                    'building:cost:create',
                    kwargs={'building_pk': building_instance.pk}
                )
            )
    else:
        building_form = BuildingForm()
        sponsor_form = SponsorForm()
        broker_form = BrokerForm()

    context = {
        'building_form': building_form,
        'sponsor_form': sponsor_form,
        'broker_form': broker_form
    }

    return render(request, template, context)


def loan_update_description(request, loan_pk):
    template = 'loan_update.html'
    loan = Loan.objects.get(pk=loan_pk)
    loan_building = Building.objects.get(pk=loan.building.pk)
    loan_sponsor = Sponsor.objects.get(pk=loan.sponsor.pk)
    loan_broker = Broker.objects.get(pk=loan.broker.pk)
    if request.method == 'POST':
        building_form = BuildingUpdateForm(request.POST, instance=loan_building)
        sponsor_form = SponsorForm(request.POST, instance=loan_sponsor)
        broker_form = BrokerForm(request.POST, instance=loan_broker)
        if building_form.is_valid() and sponsor_form.is_valid() and broker_form.is_valid():
            building_instance = building_form.save()
            sponsor_instance = sponsor_form.save()
            broker_instance = broker_form.save()

            return redirect(
                reverse('building:cost:update',
                        kwargs={
                            'building_pk': building_instance.pk}
                        )
            )
    else:
        building_form = BuildingUpdateForm(instance=loan_building)
        sponsor_form = SponsorForm(instance=loan_sponsor)
        broker_form = BrokerForm(instance=loan_broker)

    context = {
        'building_form': building_form,
        'sponsor_form': sponsor_form,
        'broker_form': broker_form,
        'loan': loan
    }

    return render(request, template, context)


class LoanDeleteView(DeleteView):
    model = Loan
    pk_url_kwarg = "loan_pk"
    template_name = "loan_delete.html"
    context_object_name = "loan"
    success_url = reverse_lazy('home')

# <=====  BUILDING VIEWS =====>


class BuildingDetailView(DetailView):
    model = Building
    pk_url_kwarg = "building_pk"
    template_name = "building_detail.html"
    context_object_name = "building"

# <=====  COST VIEWS =====>


class MultipleCostCreateView(CreateView):
    model = Cost
    template_name = 'cost_update_multiple.html'

    def get(self, request, *args, **kwargs):
        context = {
            "formset": MyCostFormSet(queryset=Cost.objects.none())
        }
        return render(request, self.template_name, context)

    def post(self, request, building_pk, *args, **kwargs):
        building = Building.objects.get(pk=building_pk)
        loan = Loan.objects.get(building=building)
        formset = MyCostFormSet(data=request.POST)

        if formset.is_valid():
            costs = formset.save(commit=False)
            for cost in costs:
                cost.building = building
                cost.save()
            return redirect(
                reverse('building:cost:update',
                        kwargs={'building_pk': building.pk})
            )

        context = {"formset": formset}
        return render(request, self.template_name, context)


class BuildingCostUpdateView(UpdateView):
    model = Cost
    template_name = 'cost_update_multiple.html'

    def get(self, request, building_pk, *args, **kwargs):
        building_selected = Building.objects.get(pk=building_pk)
        costs_seleted = Cost.objects.filter(building=building_selected)
        formset = MyCostUpdateFormSet(queryset=costs_seleted)

        context = {
            "formset": formset,
            "loans": building_selected.loan_set.all()
        }
        return render(request, self.template_name, context)

    def post(self, request, building_pk, *args, **kwargs):
        print('\n post')
        building = Building.objects.get(pk=building_pk)
        formset = MyCostUpdateFormSet(data=request.POST)

        if formset.is_valid():
            costs = formset.save(commit=False)
            for cost in formset.deleted_objects:
                cost.delete()
            for cost in costs:
                cost.building = building
                cost.save()

            if len(costs) == 0:
                return redirect('building:cost:create', building.pk)
            else:
                return redirect('building:cost:update', building.pk)

        context = {"formset": formset}
        return render(request, self.template_name, context)


class CostDeleteView(DeleteView):
    model = Cost
    template_name = "confirm_delete.html"
    pk_url_kwarg = "cost_pk"

    def get_success_url(self):
        return reverse(
            'building:cost:update', kwargs={
                'building_pk': self.object.building.pk
            })
