from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
#from trading import ...

# 0               id  d9964477-37cd-4ed6-8c40-67e814d12ee1
# 1            price                                 10000
# 2             size                                 0.001
# 3       product_id                               BTC-USD
# 4             side                                   buy
# 5              stp                                    dc
# 6             type                                 limit
# 7    time_in_force                                   GTC
# 8        post_only                                 False
# 9       created_at           2023-08-17T02:33:46.597031Z
# 10       fill_fees                                     0
# 11     filled_size                                     0
# 12  executed_value                                     0
# 13          status                               pending
# 14         settled                                 False
    
class HotBot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    currency = models.CharField(max_length=50)
    bot_run_time = models.IntegerField()
    desired_ROI = models.DecimalField(max_digits=20, decimal_places=10)
    stop_loss = models.DecimalField(max_digits=20, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.currency} HotBot (owned by {self.owner})"

    def get_absolute_url(self):
        return reverse("home")

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    size = models.DecimalField(max_digits=20, decimal_places=10)
    product_id = models.CharField(max_length=50)
    side = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.transaction_id

## Elphnt SQL -> send dataa from trading.py for tests. Identify the real tables 
## IMPORT trading and save in tables
## ADD CLASS to serialize data (django REST)
## Class to represent a model and saved into DB
