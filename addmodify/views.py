# from django.shortcuts import render
# from .models import *
# import psycopg2
#
# # Create your views here.
#
#
# def add(request):
#     if request.method == 'POST':
#         contactList = Contact.objects.all()
#         contact_id =contactList.len()+1
#         contact = Contact()
#         contact.fname = request.POST['fname']
#         contact.mname = request.POST['mname']
#         contact.lname = request.POST['lname']
#         address = Address()
#         address.contact_id = contact_id
#         address.address_type = request.POST['address_type']
#         address.address = request.POST['address']
#         address.city = request.POST['city']
#         address.state = request.POST['state']
#         address.zip = request.POST['zip']
#         phone = PhoneNumber()
#         phone.contact_id = contact_id
#         phone.phone_type = request.POST['phone_type']
#         phone.area_code = request.POST['area_code']
#         phone.number = request.POST['number']
#         date = Date()
#         date.contact_id = contact_id
#         date.date_type = request.POST['date_type']
#         date.date = request.POST['date']
#     else:
#         return render(request, 'add.html')
#
# def modify(request):
#     contact_id = request.POST['contact_id']
#     print(contact_id)
#     contact = Contact.objects.get(contact_id=contact_id)
#     addressList = Address.objects.filter(contact_id=contact_id)
#     phoneList = PhoneNumber.objects.filter(contact_id=contact_id)
#     dateList = Date.objects.filter(contact_id=contact_id)
#     personalInfo = PersonalInfo()
#     personalInfo.contact = contact
#     personalInfo.addressList = addressList
#     personalInfo.phoneList = phoneList
#     personalInfo.dateList = dateList
#     return render(request, 'modify.html', {'personalInfo': personalInfo})
#
# def delete(request):
#     return render(request, 'index.html')