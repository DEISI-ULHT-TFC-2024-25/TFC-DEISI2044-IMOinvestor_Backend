from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from .models import ROICalculation
from .serializers import ROICalculationSerializer
from rest_framework.exceptions import MethodNotAllowed


class ROICalculationViewSet(viewsets.ModelViewSet):

    queryset = ROICalculation.objects.all()
    serializer_class = ROICalculationSerializer
    permission_classes = [AllowAny]

    def calculate_roi(self, data):
        purchase_price = float(data.get("purchase_price", 0))
        closing_costs = float(data.get("closing_costs", 0))
        repair_costs = float(data.get("repair_costs", 0))
        after_repair_value = float(data.get("after_repair_value", 0))
        holding_costs = float(data.get("holding_costs", 0))
        selling_costs = float(data.get("selling_costs", 0))

        total_cost = purchase_price + closing_costs + repair_costs + holding_costs + selling_costs
        profit = after_repair_value - total_cost
        investment = purchase_price + closing_costs + repair_costs
        roi = (profit / investment) * 100 if investment != 0 else 0

        return roi, profit

    def perform_create(self, serializer):
        roi, profit = self.calculate_roi(self.request.data)
        serializer.save(roi_result=roi, profit=profit)

    def perform_update(self, serializer):
        roi, profit = self.calculate_roi(self.request.data)
        serializer.save(roi_result=roi, profit=profit)

    @swagger_auto_schema(operation_summary="Listar ROI")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Criar ROI")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Obter ROI por ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Atualizar ROI")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Excluir ROI")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
