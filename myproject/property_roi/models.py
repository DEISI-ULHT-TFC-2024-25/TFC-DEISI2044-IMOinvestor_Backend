from django.db import models

class ROICalculation(models.Model):
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    closing_costs = models.DecimalField(max_digits=12, decimal_places=2)
    repair_costs = models.DecimalField(max_digits=12, decimal_places=2)
    after_repair_value = models.DecimalField(max_digits=12, decimal_places=2)
    holding_costs = models.DecimalField(max_digits=12, decimal_places=2)
    selling_costs = models.DecimalField(max_digits=12, decimal_places=2)
    roi_result = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roi_calculations'
