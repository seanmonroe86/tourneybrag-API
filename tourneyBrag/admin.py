from django.contrib import admin

from .models import *

admin.site.register(Player)
admin.site.register(Organizer)
admin.site.register(Administrator)
admin.site.register(Tournament)
admin.site.register(Fan)
admin.site.register(Voucher)
admin.site.register(Entrant)
admin.site.register(Record)
admin.site.register(Banned)

# Register your models here.
