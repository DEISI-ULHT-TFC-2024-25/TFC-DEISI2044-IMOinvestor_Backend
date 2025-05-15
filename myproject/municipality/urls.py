from django.urls import path
from .views import MunicipalitiesByDistrictView,AllMunicipalitiesView

urlpatterns = [
    path('municipalityByDistrict/', MunicipalitiesByDistrictView.as_view(), name='municipalities-by-district'),
    path('allMunicipalities/', AllMunicipalitiesView.as_view(), name='all-municipalities'),
]
