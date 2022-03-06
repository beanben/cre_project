from django.contrib import admin
from .models.loan import Loan
from .models.cost import Cost

admin.site.register(Loan)
admin.site.register(Cost)
