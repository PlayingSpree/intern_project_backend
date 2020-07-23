from rest_framework import filters


class MultiSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        for s in getattr(view, 'search_fields', None):
            if view.action in s[0]:
                return s[1]
