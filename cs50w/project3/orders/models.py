from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=50, default="new")

    def __str__(self):
        return (f"{self.name}")


class Part(models.Model):
    name = models.CharField(max_length=50, default="new")

    def __str__(self):
        return (f"{self.name}")


class Extra(models.Model):
    name = models.CharField(max_length=50, default="new")
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)

    def __str__(self):
        return (f"{self.name} {self.price}")


class Product(models.Model):
    
    class ExtraList(models.IntegerChoices):
        NO_EXTRAS = 0
        WITH_EXTRAS = 999

    class PartList(models.IntegerChoices):
        NO_TOPPING = 0
        ONE_TOPPING = 1
        TWO_TOPPINGS = 2
        THREE_TOPPINGS = 3

    name = models.CharField(max_length=50, default="new")
    category = models.ForeignKey(Group, on_delete=models.PROTECT, related_name="items")
    extras = models.IntegerField(choices=ExtraList.choices, default=0)
    parts = models.IntegerField(choices=PartList.choices, default=0)

    def __str__(self):
        return (f"{self.category} {self.name}")


class Offer(models.Model):
    name = models.CharField(max_length=30, default="", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    owner = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="types")

    def __str__(self):
        return (f"{self.owner} {self.name} {self.price}")


class OrderHeader(models.Model):
    client = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    status = models.CharField(max_length=30) 
    stamp = models.CharField(max_length=30)

    def __str__(self):
        return (f"{self.id} {self.client} {self.total} {self.stamp[:16]} {self.status}")


class OrderDetail(models.Model):
    oid = models.ForeignKey(OrderHeader, on_delete=models.PROTECT, related_name="orderdetails")
    name = models.CharField(max_length=120)
    namex = models.CharField(max_length=120, default="", blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    pricex = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    gid = models.IntegerField(default=0)
    pid = models.IntegerField(default=0)
    tid = models.IntegerField(default=0)

    def __str__(self):
        return (f"{self.id} {self.oid} {self.name} {self.namex} {self.quantity} {self.total}")
