from django.urls import path
from .views import ROICalculationCreateView

urlpatterns = [
    path("calculate/", ROICalculationCreateView.as_view(), name="calculate-roi"),
]
