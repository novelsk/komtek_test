from django.contrib import admin
from django.db import models

from .models import Reference, ReferenceVersion, ReferenceElement


class ReferenceVersionInline(admin.TabularInline):
    model = ReferenceVersion
    fields = ('id', 'code', 'start_date')
    show_change_link = True


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
        'name',
        'active__version',
        'active__start_date'
    )
    search_fields = ('code', 'name')
    inlines = (ReferenceVersionInline,)

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .prefetch_related(models.Prefetch(
                'versions',
                queryset=ReferenceVersion.objects.order_by('-start_date')[:1],
                to_attr='active_version',
            ))
        )

    @staticmethod
    @admin.display(description='Версия')
    def active__version(obj):
        if obj.active_version:
            return obj.active_version[0].code

    @staticmethod
    @admin.display(description='Дата начала действия версии')
    def active__start_date(obj):
        if obj.active_version and obj.active_version[0].start_date is not None:
            return obj.active_version[0].start_date.strftime("%d.%m.%Y")


@admin.register(ReferenceVersion)
class ReferenceVersionAdmin(admin.ModelAdmin):
    list_display = (
        'reference__code',
        'reference__name',
        'code',
        'start_date'
    )
    search_fields = ('code',)
    autocomplete_fields = ('reference',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reference')

    @staticmethod
    @admin.display(description='Код')
    def reference__code(self):
        return self.reference.code

    @staticmethod
    @admin.display(description='Наименование')
    def reference__name(self):
        return self.reference.name


@admin.register(ReferenceElement)
class ReferenceElementAdmin(admin.ModelAdmin):
    autocomplete_fields = ('version',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('version')
