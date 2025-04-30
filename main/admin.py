from django.contrib import admin
from .models import Stock, Purchase, CurrentPrice  # ✅ Correct class names

admin.site.register(Stock)
admin.site.register(Purchase)
admin.site.register(CurrentPrice)
