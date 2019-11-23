import csv
from django.contrib import admin
from accounts.models import profile,Friend,add_group
from django.utils.encoding import smart_str
# Register your models here.

admin.site.register(profile)
admin.site.register(Friend)
#admin.site.register(add_group)

class add_groupAdmin(admin.ModelAdmin):
	#actions = [export_csv]

	def export_csv(modeladmin, request, queryset):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
		writer = csv.writer(response, csv.excel)
		response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
		writer.writerow([smart_str(u"GroupName"),smart_str(u"Description"),])
		for obj in queryset:
			writer.writerow([smart_str(obj.GroupName),smart_str(obj.Description),])
		return response
		export_csv.short_description = u"Export CSV"

admin.site.register(add_group,add_groupAdmin)