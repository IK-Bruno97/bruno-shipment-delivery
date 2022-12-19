from django.db import models

# Create your models here.
class Shipment(models.Model):
    date = models.DateField(auto_now_add=True, null=True)
    email = models.EmailField(null=False, blank=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=30, null=True, blank=True)
    package = models.CharField(max_length=50, null=False, blank=False)
    origin = models.CharField(max_length=100, null=True, blank=False)
    destination = models.CharField(max_length=100, null=True, blank=False)
    weight = models.DecimalField(max_digits=10, decimal_places=2 ,null=False, blank=False)
    tracking_number = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.email+ ". Item to ship:" +self.package 