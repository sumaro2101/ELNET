from rest_framework.pagination import PageNumberPagination


class BasePaginate(PageNumberPagination):
    """Постраничный базовый вывод (10 объектов)
    """
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 25
