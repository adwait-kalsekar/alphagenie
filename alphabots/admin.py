from django.contrib import admin

# Register your models here.
from .models import StockSymbol, Bucket, Strategy, KPI, Backtesting, TradingBot, Investment

admin.site.register(StockSymbol)
admin.site.register(Bucket)
admin.site.register(Strategy)
admin.site.register(KPI)
admin.site.register(Backtesting)
admin.site.register(TradingBot)
admin.site.register(Investment)