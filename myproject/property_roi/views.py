from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import ROICalculation
from .serializers import ROICalculationSerializer

class ROICalculationCreateView(generics.CreateAPIView):
    queryset = ROICalculation.objects.all()
    serializer_class = ROICalculationSerializer

    def perform_create(self, serializer):
        data = self.request.data
        purchase_price = float(data.get("purchase_price", 0))
        closing_costs = float(data.get("closing_costs", 0))
        repair_costs = float(data.get("repair_costs", 0))
        after_repair_value = float(data.get("after_repair_value", 0))
        holding_costs = float(data.get("holding_costs", 0))
        selling_costs = float(data.get("selling_costs", 0))

        total_cost = purchase_price + closing_costs + repair_costs + holding_costs + selling_costs
        profit = after_repair_value - total_cost
        roi = (profit / (purchase_price + closing_costs + repair_costs)) * 100 if (purchase_price + closing_costs + repair_costs) != 0 else 0

        serializer.save(roi_result=roi, profit=profit)
