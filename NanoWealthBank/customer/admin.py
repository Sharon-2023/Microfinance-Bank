from django.contrib import admin
from customer.models import (Admin, Current, Customer, FixedDeposit, Loan, LoanOfficer, Savings,
    Transaction)

# Register your models here.
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(LoanOfficer)
admin.site.register(Savings)
admin.site.register(Current)
admin.site.register(Loan)
admin.site.register(Transaction)
admin.site.register(FixedDeposit)
