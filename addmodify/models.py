# from django.db import models
#
# # Create your models here.
# class Contact(models.Model):
#     contact_id = models.AutoField(primary_key=True)
#     fname = models.CharField(max_length=100)
#     mname = models.CharField(max_length=100)
#     lname = models.CharField(max_length=100)
#
# class Address(models.Model):
#     address_id = models.AutoField(primary_key=True)
#     contact_id = models.IntegerField()
#     address_type = models.CharField(max_length=100)
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     zip = models.CharField(max_length=10)
#
# class PhoneNumber(models.Model):
#     phone_id = models.AutoField(primary_key=True)
#     contact_id = models.IntegerField()
#     phone_type = models.CharField(max_length=100)
#     area_code = models.CharField(max_length=3)
#     number = models.CharField(max_length=7)
#
# class Date(models.Model):
#     date_id = models.AutoField(primary_key=True)
#     contact_id = models.IntegerField()
#     date_type = models.CharField(max_length=100)
#     date = models.DateField()
#
# class PersonalInfo:
#     contact: Contact
#     addressList: []
#     phoneList: []
#     dateList: []