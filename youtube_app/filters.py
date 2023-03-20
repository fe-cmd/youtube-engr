import django_filters

from .models import Filters


class FiltersFilter(django_filters.FilterSet):

    class Meta:
        model = Filters
        fields = [
            'sortby',
            'features', 
            'duration',
            'type',
            'upload_date',
        ]