from django.contrib import admin
from accounts.models import profile,Friend,Add_group,Transactions,Pair,Group_Transactions
# Register your models here.

admin.site.register(profile)
admin.site.register(Friend)
admin.site.register(Add_group)
admin.site.register(Transactions)
admin.site.register(Pair)
admin.site.register(Group_Transactions)
