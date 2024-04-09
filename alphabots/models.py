from django.db import models
from django.contrib.auth.models import User
from alphatrader.models import TraderProfile

# Create your models here.

class StockSymbol(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.symbol

class Bucket(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symbols = models.ManyToManyField(StockSymbol)
    user = models.ForeignKey(TraderProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Strategy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Backtesting(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bot = models.ForeignKey('TradingBot', on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TradingBot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(TraderProfile, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    is_deployed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Investment(models.Model):
    bot = models.ForeignKey('TradingBot', on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    investment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.bot.name}+{self.investment_date}"
