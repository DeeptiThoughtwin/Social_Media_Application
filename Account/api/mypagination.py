from rest_framework.pagination import PageNumberPagination

class myPagePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page'
    max_page_size = 5