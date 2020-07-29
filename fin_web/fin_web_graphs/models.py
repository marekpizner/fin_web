from django.db import models


class BTC(models.Model):
    date = models.DateField()
    value = models.FloatField()
    btc_count = models.IntegerField()
    btc_mining_diff = models.FloatField()

    def __str__(self):
        return str(self.date)
