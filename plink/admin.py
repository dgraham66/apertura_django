from django.contrib import admin

from models import Plink
from models import PlinkJob
from models import PlinkOption

# Register your models here.


admin.site.register(Plink)
admin.site.register(PlinkJob)
admin.site.register(PlinkOption)
