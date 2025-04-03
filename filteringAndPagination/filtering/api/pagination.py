from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class bookPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 8

class bookLOPagination(LimitOffsetPagination):
    default_limit = 3

class bookCPagination(CursorPagination):
    page_size = 2
    ordering = 'Published_date'

