import django_filters
from .models import Announcement

class AnnouncementFilter(django_filters.FilterSet):
    district = django_filters.NumberFilter(field_name="property__district__id", lookup_expr="exact")
    municipality = django_filters.NumberFilter(field_name="property__municipality__id", lookup_expr="exact")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    property_type = django_filters.CharFilter(field_name="property__property_type", lookup_expr='iexact')
    area_bruta = django_filters.NumberFilter(field_name="property__area_bruta", lookup_expr='gte')
    area_util = django_filters.NumberFilter(field_name="property__area_util", lookup_expr='gte')
    nova_construcao = django_filters.CharFilter(field_name="property__nova_construcao", lookup_expr='exact')
    numero_casas_banho = django_filters.CharFilter(field_name="property__numero_casas_banho", lookup_expr='exact')
    tipologia = django_filters.CharFilter(field_name="property__tipologia", lookup_expr='exact')
    certificado_energetico = django_filters.CharFilter(field_name="property__certificado_energetico", lookup_expr='exact')

    class Meta:
        model = Announcement
        fields = [
            'district',
            'municipality',
            'price_min',
            'price_max',
            'property_type',
            'area_bruta',
            'area_util',
            'nova_construcao',
            'numero_casas_banho',
            'tipologia',
            'certificado_energetico',
        ]
