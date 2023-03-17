
from django.db import models
from django.contrib.auth.models import User

DATA_TYPE_CHOICES = [
        ('full_name', 'Full name'),
        ('job', 'Job'),
        ('email', 'Email'),
        ('domain_name', 'Domain name'),
        ('phone_number', 'Phone number'),
        ('company_name', 'Company name'),
        ('text', 'Text'),
        ('integer', 'Integer'),
        ('address', 'Address'),
        ('date', 'Date'),
    ]


class DataSchema(models.Model):
    """
    A model for Data Schemas.
    """
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True)
    modified_at = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class DataColumn(models.Model):
    """
    A model for Data Columns
    """
    data_schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE, related_name='schema_column')
    name = models.CharField(max_length=50)
    data_type = models.CharField(max_length=50, choices=DATA_TYPE_CHOICES)
    sentences_num = models.IntegerField(default=1)
    start_num = models.IntegerField(blank=True, null=True, default=1)
    end_num = models.IntegerField(blank=True, null=True, default=10)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    """
    A model for Datasets
    """
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('ready', 'Ready')
    )

    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE, related_name="data_schema")
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='processing')
    num_of_records = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True, null=True)
    modified_at = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return str(self.modified_at)
