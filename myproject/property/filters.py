import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    district = django_filters.NumberFilter(field_name="district__id", lookup_expr="exact")
    municipality = django_filters.NumberFilter(field_name="municipality__id", lookup_expr="exact")
    area_bruta = django_filters.NumberFilter(field_name="area_bruta", lookup_expr='exact')
    area_util = django_filters.NumberFilter(field_name="area_util", lookup_expr='exact')
    nova_construcao = django_filters.CharFilter(field_name="nova_construcao", lookup_expr='iexact')
    property_type = django_filters.CharFilter(field_name="property_type", lookup_expr='iexact')
    preco_minimo = django_filters.NumberFilter(field_name="preco_minimo", lookup_expr='gte')
    preco_maximo = django_filters.NumberFilter(field_name="preco_maximo", lookup_expr='lte')

    class Meta:
        model = Property
        fields = []
