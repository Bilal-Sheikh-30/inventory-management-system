from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class Department(models.Model):
    deptName = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.deptName}'
    
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
    
class Category(models.Model):
    category_status_choices = [('sus','suspended'),('cont','continue'),]
    categoryName = models.CharField(max_length=50)
    categoryStatus = models.CharField(max_length=4, choices = category_status_choices, default='cont')  

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.categoryName
    
class Item(models.Model):
    item_nature_choices = [('sus','suspended'),('cont','continue'),]

    Item_name = models.CharField(max_length=100)
    Category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    min_qty = models.IntegerField()
    max_qty = models.IntegerField()
    instock_qty = models.IntegerField()
    rack_no = models.CharField(max_length=100, null=True, blank=True)
    bin_no = models.CharField(max_length=100, null=True, blank=True)
    item_status = models.CharField(max_length=50, blank=True)
    item_nature = models.CharField(max_length=4, choices = item_nature_choices, default='cont')  

    def __str__(self):
        return self.item_name
    
class Vendor(models.Model):
    vendor_status_options = [('active','active'),('inactive','inactive'),]

    vendor_name = models.CharField(max_length=50)
    vendor_email = models.EmailField(unique=True)
    vendor_phoneNo = models.CharField(max_length=11)
    categories = models.ManyToManyField(Category, blank=True, related_name='vendors')
    items = models.ManyToManyField(Item, blank=True, related_name='vendors')
    vendor_status = models.CharField(max_length=10,choices=vendor_status_options, default='active')
    remarks = models.CharField(max_length=100, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor_name
    
class Requests(models.Model):
    requestBy = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    item_id = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    qty_required = models.IntegerField()
    status = models.CharField(max_length=100)
    remarks = models.CharField(max_length=500,null=True)

class Orders(models.Model):
    orderBy = models.ForeignKey(CustomUser, null=True,on_delete=models.SET_NULL, related_name='order_by')
    requestID = models.ForeignKey(Requests, null=True,on_delete=models.SET_NULL)
    receiveBy = models.ForeignKey(CustomUser, null=True,on_delete=models.SET_NULL, related_name='receive_by')
    vendorNo = models.ForeignKey(Vendor, null=True,on_delete=models.SET_NULL)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    totalPrice = models.IntegerField()
    orderDate = models.DateTimeField(auto_now_add=True)
    expectedDeliveryDate = models.DateField()
    receivingDate = models.DateField()
    status = models.CharField(max_length=50)
    remarks = models.CharField(max_length=100, null=True)

class ItemIssue(models.Model):
    issueBy = models.ForeignKey(CustomUser, null=True,on_delete=models.SET_NULL)
    issueTo = models.CharField(max_length=100)
    issue_to_dept = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    item_id = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    qty_issued = models.IntegerField()
    issueDate = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=100, null=True)

class ItemLedger(models.Model):
    date = models.DateField()
    orderNo = models.ForeignKey(Orders, null=True, on_delete=models.SET_NULL)
    gate_pass_no = models.ForeignKey(ItemIssue, null=True, on_delete=models.SET_NULL)
    opening_balance = models.IntegerField()
    balance_received = models.IntegerField()
    balance_issued = models.IntegerField()
    closing_balance = models.IntegerField()
    status = models.CharField(max_length=50)

    

