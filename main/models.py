from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True, db_index=True)  # Already unique, but db_index helps
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.symbol

class Purchase(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, db_index=True)  # Good for JOINs
    quantity = models.PositiveIntegerField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['stock', 'buy_price']),
        ]

    def __str__(self):
        return f"{self.stock.symbol} - {self.quantity} @ {self.buy_price}"

class CurrentPrice(models.Model):
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock.symbol} = {self.current_price}"
