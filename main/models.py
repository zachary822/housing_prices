from django.db import models


# Create your models here.
class Borough(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    borough = models.ForeignKey(Borough, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    price = models.BigIntegerField(db_index=True)
    date = models.DateTimeField()
