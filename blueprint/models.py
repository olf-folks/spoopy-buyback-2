from django.db import models

# Create your models here.

class BlueprintBase(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class BlueprintVersion(models.Model):
    blueprint = models.ForeignKey(BlueprintBase, on_delete=models.CASCADE)
    version_number = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    # Version-specific stats
    stat1 = models.IntegerField()
    stat2 = models.IntegerField()
    stat3 = models.IntegerField()
    
    # Blueprint runs, material efficiency, and time efficiency
    runs = models.PositiveIntegerField()
    material_efficiency = models.PositiveIntegerField()
    time_efficiency = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.blueprint} - Version {self.version_number}"
