from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .models.property import Property, PropertyForm, PropertyUpdateForm
from .models.sponsor import Sponsor, SponsorForm
from .models.deal import Deal, DealForm
from .models.broker import Broker, BrokerForm
import pdb


def home(request):
    context = {
        'deals': Deal.objects.all(),
    }
    return render(request, 'cre_finance/home.html', context)

# <=====  SPONSOR VIEWS =====>


class SponsorCreateView(CreateView):
    model = Sponsor
    form_class = SponsorForm
    template_name = 'sponsor_create.html'
    success_url = reverse_lazy('home')


class SponsorUpdateView(UpdateView):
    model = Sponsor
    form_class = SponsorForm
    pk_url_kwarg = "sponsor_pk"
    template_name = "sponsor_update.html"

    def get_success_url(self):
        return reverse('sponsor:update', args={self.object.pk})


class SponsorDeleteView(DeleteView):
    model = Sponsor
    pk_url_kwarg = "sponsor_pk"
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('home')

# <=====  PROPERTY VIEWS =====>


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

# <=====  DEAL VIEWS =====>


def deal_create(request):
    template = 'deal_create.html'
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        sponsor_form = SponsorForm(request.POST)
        broker_form = BrokerForm(request.POST)
        if property_form.is_valid() and sponsor_form.is_valid() and broker_form.is_valid():
            property_instance = property_form.save()
            sponsor_instance = sponsor_form.save()
            broker_instance = broker_form.save()
            deal = Deal.objects.create(
                sponsor=sponsor_instance,
                property=property_instance,
                broker=broker_instance
            )
            return redirect('home')
    else:
        property_form = PropertyForm()
        sponsor_form = SponsorForm()
        broker_form = BrokerForm()

    context = {
        'property_form': property_form,
        'sponsor_form': sponsor_form,
        'broker_form': broker_form
    }

    return render(request, template, context)


# def deal_update(request, deal_pk):
#     template = 'deal_update.html'
#     deal = Deal.objects.get(pk=deal_pk)
#     property_instance = Property.objects.get(pk=deal.property.pk)
#     print('\n deal:', deal)
#     print('property_instance:', property_instance)

# class DealCreateView(CreateView):
#     model = Deal
#     form_class = DealForm
#     template_name = 'deal_create.html'
#     success_url = reverse_lazy('home')
#
def deal_update(request, deal_pk):
    template = 'deal_update.html'
    deal = Deal.objects.get(pk=deal_pk)
    deal_property = Property.objects.get(pk=deal.property.pk)
    deal_sponsor = Sponsor.objects.get(pk=deal.sponsor.pk)
    deal_broker = Broker.objects.get(pk=deal.broker.pk)
    if request.method == 'POST':
        property_form = PropertyUpdateForm(request.POST, instance=deal_property)
        sponsor_form = SponsorForm(request.POST, instance=deal_sponsor)
        broker_form = BrokerForm(request.POST, instance=deal_broker)
        if property_form.is_valid() and sponsor_form.is_valid() and broker_form.is_valid():
            property_instance = property_form.save()
            sponsor_instance = sponsor_form.save()
            broker_instance = broker_form.save()

            return redirect(reverse('deal:update', kwargs={'deal_pk': deal_pk}))
    else:
        property_form = PropertyUpdateForm(instance=deal_property)
        sponsor_form = SponsorForm(instance=deal_sponsor)
        broker_form = BrokerForm(instance=deal_broker)

    context = {
        'property_form': property_form,
        'sponsor_form': sponsor_form,
        'broker_form': broker_form,
        'deal_property': deal_property,
    }
    print("deal_property.longitude:", deal_property.longitude)

    return render(request, template, context)


class DealUpdateView(UpdateView):
    model = Deal
    form_class = DealForm
    pk_url_kwarg = "deal_pk"
    template_name = "deal_update.html"
    context_object_name = "deal"

    def get_success_url(self):
        return reverse('deal:update', args={self.object.pk})


class DealDeleteView(DeleteView):
    model = Deal
    pk_url_kwarg = "deal_pk"
    template_name = "deal_delete.html"
    context_object_name = "deal"
    success_url = reverse_lazy('home')
