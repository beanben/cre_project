from django.contrib import admin
from .models.cost import Cost
from .models.building import Building
from .models.loan import Loan

admin.site.register(Cost)
admin.site.register(Building)
admin.site.register(Loan)
