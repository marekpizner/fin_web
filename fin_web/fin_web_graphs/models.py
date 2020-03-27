from django.db import models


# Create your models here.

class Olhc(models.Model):
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()
    market_cap = models.IntegerField()

    def __str__(self):
        return str(self.date)


class BTC(models.Model):
    date = models.DateField()
    value = models.FloatField()
    btc_count = models.IntegerField()
    btc_mining_diff = models.FloatField()
