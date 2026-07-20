from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    # Количество элементов на одной странице по умолчанию
    page_size = 5
    # Переменная для изменения количества
    page_size_query_param = "page_size"
    # Максимальный лимит
    max_page_size = 50
