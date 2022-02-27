from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .models.building import Building, BuildingForm, BuildingUpdateForm
from .models.sponsor import Sponsor, SponsorForm
from .models.loan import Loan
from .models.broker import Broker, BrokerForm
from .models.cost import Cost, CostForm
import pdb


def home(request):
    context = {
        'loans': Loan.objects.all(),
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
            return redirect('home')
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
                reverse('loan:building_costs:create',
                        kwargs={'loan_pk': loan_pk})
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

# <=====  COST VIEWS =====>


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
            return redirect('building:create', loan_pk=loan_pk)

        context = {"formset": formset}
        return render(request, self.template_name, context)
