from django.contrib import admin
from .models import Sucursal
# Register your models here.

@admin.register(Sucursal)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['nombre','pais','telefono']
    search_fields = ['nombre','pais']
    list_display = ['pais']