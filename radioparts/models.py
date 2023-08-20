from django.db import models
from django.contrib.auth.models import User

class RadioPart(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='radio_parts/', null=True, blank=True)  # Add this field

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part = models.ForeignKey(RadioPart, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.part.name}"
