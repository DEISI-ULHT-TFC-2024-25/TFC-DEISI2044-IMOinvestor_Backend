from django.urls import path
from .views import MunicipalitiesByDistrictView

urlpatterns = [
    path('municipalityByDistrict/', MunicipalitiesByDistrictView.as_view(), name='municipalities-by-district'),
]
