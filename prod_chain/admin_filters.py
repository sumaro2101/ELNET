from typing import Any
from django.contrib.admin import SimpleListFilter

from django.db.models.query import QuerySet
from django_countries import countries


class CountiesListFilter(SimpleListFilter):
    """Фильтрация по стране в админ панели
    """
    title = 'Страны'
    parameter_name = 'country'

    def lookups(self,
                request,
                model_admin) -> list[tuple[Any, str]]:
        return [(code, country)
                 for code, country
                 in countries.countries.items()]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if not self.value():
            return None
        return queryset.filter(prod_object__country=self.value())
