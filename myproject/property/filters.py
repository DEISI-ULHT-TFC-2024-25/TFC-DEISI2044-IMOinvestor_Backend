import django_filters
from django_filters import ChoiceFilter
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    district = django_filters.NumberFilter(field_name="district__id", lookup_expr="exact")
    municipality = django_filters.NumberFilter(field_name="municipality__id", lookup_expr="exact")
    area_bruta = django_filters.NumberFilter(field_name="area_bruta", lookup_expr='gte')
    area_util = django_filters.NumberFilter(field_name="area_util", lookup_expr='gte')
    property_type = ChoiceFilter(field_name="property_type", choices=Property.TIPO_CHOICE)
    nova_construcao = ChoiceFilter(field_name="nova_construcao", choices=Property.NOVA_CONSTRUCAO_CHOICES)
    certificado_energetico = ChoiceFilter(field_name="certificado_energetico", choices=Property.CERTIFICADO_CHOICES)

    preco_minimo = django_filters.NumberFilter(field_name="preco_minimo", lookup_expr='gte')
    preco_maximo = django_filters.NumberFilter(field_name="preco_maximo", lookup_expr='lte')
    
    tipologia = django_filters.CharFilter(field_name="tipologia", lookup_expr='exact')
    numero_casas_banho = django_filters.CharFilter(field_name="numero_casas_banho", lookup_expr='exact')

    class Meta:
        model = Property
        fields = [ ]
