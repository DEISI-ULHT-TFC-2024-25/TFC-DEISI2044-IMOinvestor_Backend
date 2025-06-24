import django_filters
from .models import Announcement

class AnnouncementFilter(django_filters.FilterSet):
    district = django_filters.NumberFilter(field_name="property__district__id", lookup_expr="exact")
    municipality = django_filters.NumberFilter(field_name="property__municipality__id", lookup_expr="exact")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    property_type = django_filters.CharFilter(field_name="property__property_type", lookup_expr='iexact')
    gross_area = django_filters.NumberFilter(field_name="property__gross_area", lookup_expr='gte')
    net_area = django_filters.NumberFilter(field_name="property__net_area", lookup_expr='gte')
    new_construction = django_filters.CharFilter(field_name="property__new_construction", lookup_expr='exact')
    num_wc = django_filters.CharFilter(field_name="property__num_wc", lookup_expr='exact')
    typology = django_filters.CharFilter(field_name="property__typology", lookup_expr='exact')
    energy_certf = django_filters.CharFilter(field_name="property__energy_certf", lookup_expr='exact')
    is_active = django_filters.BooleanFilter(field_name="is_active", lookup_expr='exact')



    

    
    class Meta:
        model = Announcement
        fields = [
            'district',
            'municipality',
            'price_min',
            'price_max',
            'property_type',
            'gross_area',
            'net_area',
            'new_construction',
            'num_wc',
            'typology',
            'energy_certf',
            'is_active',
        ]
