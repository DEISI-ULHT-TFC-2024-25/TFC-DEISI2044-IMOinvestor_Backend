import django_filters
from .models import Announcement

class AnnouncementFilter(django_filters.FilterSet):
    district = django_filters.NumberFilter(field_name="property__district__id", lookup_expr="exact")
    municipality = django_filters.NumberFilter(field_name="property__municipality__id", lookup_expr="exact")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    property_type = django_filters.CharFilter(field_name="property__property_type", lookup_expr='iexact')

    class Meta:
        model = Announcement
        fields = ["district", "municipality", "price_min", "price_max", "property_type"]
