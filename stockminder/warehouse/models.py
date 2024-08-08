from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class Department(models.Model):
    deptName = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.id}. {self.deptName}'
    
    
class CustomUser(AbstractUser):
    STATUS_CHOICES = [
        ('NA', 'None'),
        ('SO', 'Store Officer'),
        ('PO', 'Procurement Officer'),
        ('FO', 'Finance Officer'),
    ]

    DeptId = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NA')
    registerDate = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status != 'NA' and self.registerDate is None:
            self.registerDate = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'EMP-{self.id} {self.first_name} {self.last_name}'
    