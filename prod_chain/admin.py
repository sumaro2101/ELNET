from django.contrib import admin
from django.utils.translation import ngettext
from django.contrib import messages

from .models import Product, ProdMap, Contact
from .admin_filters import CountiesListFilter


@admin.register(Product)
class ProductAdminView(admin.ModelAdmin):
    """Представления продукта на админ панели
    """
    list_display = ('name',
                    'model',
                    'realize',
                    )


@admin.register(ProdMap)
class ProdMapAdminView(admin.ModelAdmin):
    """Представления цепочки
    """
    list_display = ('prod_object',
                    'supplier',
                    'duty',
                    'appoiment_date',
                    )
    list_display_links = ('prod_object', 'supplier',)
    list_select_related = ('prod_object', 'supplier',)
    list_max_show_all = 50
    list_per_page = 35
    filter_horizontal = (
        'products',
    )
    list_filter = (CountiesListFilter,)
    search_fields = ('prod_object__town', 'appoiment_date')
    actions = ('clear_duty',)
    date_hierarchy = 'appoiment_date'

    @admin.action(description='Снять долги с объектов')
    def clear_duty(self, request, queryset):
        updated = queryset.update(duty=0)
        self.message_user(
            request,
            ngettext(
                "%d Долг был успешно снят.",
                "%d Долги были успешно сняты.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


@admin.register(Contact)
class ContactAdminView(admin.ModelAdmin):
    """Представление контактов
    """
    list_display = ('name',
                    'role',
                    'email',
                    'country',
                    'town',
                    'street',
                    'build',
                    )
    fieldsets = (
        ('Личная информация', {'fields': ('name', 'role', 'email')}),
        ('Локация', {'fields': ('country',
                                'town',
                                'street',
                                'build',
                                )}),
    )
    list_max_show_all = 50
    list_per_page = 35
    search_fields = ('town', 'role')
    list_filter = (CountiesListFilter,)
