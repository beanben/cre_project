from .models.property import Property, PropertyForm, PropertyUpdateForm


def home(request):
    context = {
        'properties': Property.objects.all()
    }
    return render(request, 'cre_finance/home.html', context)

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
