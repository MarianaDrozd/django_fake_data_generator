from django.contrib import admin
from .models import DataColumn, DataSchema, Dataset

# Register your models here.


class DataColumnInLineAdmin(admin.TabularInline):
    model = DataColumn


class DataSchemaAdmin(admin.ModelAdmin):
    inlines = [DataColumnInLineAdmin]


admin.site.register(DataSchema, DataSchemaAdmin)
admin.site.register(Dataset)
