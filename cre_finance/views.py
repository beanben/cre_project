from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from .models.property import Property, PropertyForm, PropertyUpdateForm
from .models.sponsor import Sponsor, SponsorForm


def home(request):
    context = {
        'properties': Property.objects.all(),
        'sponsors': Sponsor.objects.all(),
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
