from django.contrib import admin
from accounts.models import profile,Friend,add_group,Transactions
# Register your models here.

admin.site.register(profile)
admin.site.register(Friend)
admin.site.register(add_group)
admin.site.register(Transactions)
