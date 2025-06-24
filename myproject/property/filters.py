import django_filters
from django_filters import ChoiceFilter
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    district = django_filters.NumberFilter(field_name="district__id", lookup_expr="exact")
    municipality = django_filters.NumberFilter(field_name="municipality__id", lookup_expr="exact")
    gross_area = django_filters.NumberFilter(field_name="gross_area", lookup_expr='gte')
    net_area = django_filters.NumberFilter(field_name="net_area", lookup_expr='gte')
    property_type = ChoiceFilter(field_name="property_type", choices=Property.TIPO_CHOICE)
    new_construction = ChoiceFilter(field_name="new_construction", choices=Property.NOVA_CONSTRUCAO_CHOICES)
    energy_certf = ChoiceFilter(field_name="energy_certf", choices=Property.CERTIFICADO_CHOICES)

    min_price = django_filters.NumberFilter(field_name="min_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="max_price", lookup_expr='lte')
    
    typology = django_filters.CharFilter(field_name="typology", lookup_expr='exact')
    num_wc = django_filters.CharFilter(field_name="num_wc", lookup_expr='exact')

    class Meta:
        model = Property
        fields = [ ]
