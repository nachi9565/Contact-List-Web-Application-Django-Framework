import csv

from django.shortcuts import render, redirect
from .models import *
from django.utils.dateparse import parse_date
from django.db.models import Max
from django.contrib.postgres.search import SearchVector, SearchQuery

# Create your views here.
def index(request):
    # importdata()
    query = ""
    contactList = []
    if 'search_input' in request.GET and request.GET['search_input'] != '':
        query = request.GET['search_input']
        contactList = searchRecords(query)
    else:
        contactList = Contact.objects.all().order_by('contact_id')
    addressList = Address.objects.all()
    phoneList = PhoneNumber.objects.all()
    dateList = Date.objects.all()
    personalInfoList = []
    for contact in contactList:
        personalInfo = PersonalInfo()
        personalInfo.contact = contact
        personalInfoList.append(personalInfo)
    for personalInfo in personalInfoList:
        personalInfo.addressList = list(
            filter(lambda address: personalInfo.contact.contact_id == address.contact_id, addressList))
        personalInfo.phoneList = list(
            filter(lambda phone: personalInfo.contact.contact_id == phone.contact_id, phoneList))
        personalInfo.dateList = list(filter(lambda date: personalInfo.contact.contact_id == date.contact_id, dateList))

    return render(request, 'index.html', {'personalInfoList': personalInfoList,'query': str(query),'total': len(personalInfoList)})


def add(request):
    if request.method == 'POST':
        contact_id = Contact.objects.aggregate(Max('contact_id'))['contact_id__max'] + 1
        # breakpoint()
        contact = Contact()
        contact.contact_id = contact_id
        contact.fname = request.POST['fname']
        contact.mname = request.POST['mname']
        contact.lname = request.POST['lname']
        contact.save()
        address_type_list = request.POST.getlist('address_type')
        address_list = request.POST.getlist('address')
        city_list = request.POST.getlist('city')
        state_list = request.POST.getlist('state')
        zip_list = request.POST.getlist('zip')

        for i in range(len(address_type_list)):
            address = Address()
            address.contact_id = contact_id
            address.address_type = address_type_list[i]
            address.address = address_list[i]
            address.city = city_list[i]
            address.state = state_list[i]
            address.zip = zip_list[i]
            if address.address_type!='' or address.address!='' or address.city!='' or address.state!='' or address.zip!='':
                address.save()
        phone_type_list = request.POST.getlist('phone_type')
        area_code_list = request.POST.getlist('area_code')
        number_list = request.POST.getlist('number')
        for i in range(len(phone_type_list)):
            phone = PhoneNumber()
            phone.contact_id = contact_id
            phone.phone_type = phone_type_list[i]
            phone.area_code = area_code_list[i]
            phone.number = number_list[i]
            if phone.phone_type != '' or phone.area_code != '' or phone.number != '':
                phone.save()
        date_type_list = request.POST.getlist('date_type')
        date_list = request.POST.getlist('date')
        for i in range(len(date_type_list)):
            date = Date()
            date.contact_id = contact_id
            date.date_type = date_type_list[i]
            date.date = parse_date(date_list[i])
            if date.date_type != '' or date.date != '':
                date.save()
        return redirect('/')
    else:
        return render(request, 'add.html')


def modify(request):
    contact_id = request.POST['contact_id']
    contact = Contact.objects.get(contact_id=contact_id)
    addressList = Address.objects.filter(contact_id=contact_id)
    phoneList = PhoneNumber.objects.filter(contact_id=contact_id)
    dateList = Date.objects.filter(contact_id=contact_id)
    personalInfo = PersonalInfo()
    personalInfo.contact = contact
    personalInfo.addressList = addressList
    personalInfo.phoneList = phoneList
    personalInfo.dateList = dateList
    return render(request, 'modify.html', {'personalInfo': personalInfo})

def modifysubmit(request):
    contact = Contact()
    contact.contact_id = request.POST['contact_id']
    contact.fname = request.POST['fname']
    contact.mname = request.POST['mname']
    contact.lname = request.POST['lname']
    contact.save()
    address_id_list = request.POST.getlist('address_id')
    address_type_list = request.POST.getlist('address_type')
    address_list = request.POST.getlist('address')
    city_list = request.POST.getlist('city')
    state_list = request.POST.getlist('state')
    zip_list = request.POST.getlist('zip')
    # breakpoint()
    for i in range(len(address_type_list)):
        address = Address()
        if i < len(address_id_list):
            address.address_id = address_id_list[i]
        address.contact_id = contact.contact_id
        address.address_type = address_type_list[i]
        address.address = address_list[i]
        address.city = city_list[i]
        address.state = state_list[i]
        address.zip = zip_list[i]
        address.save()
    phone_id_list = request.POST.getlist('phone_id')
    phone_type_list = request.POST.getlist('phone_type')
    area_code_list = request.POST.getlist('area_code')
    number_list = request.POST.getlist('number')
    for i in range(len(phone_type_list)):
        phone = PhoneNumber()
        if i < len(phone_id_list):
            phone.phone_id = phone_id_list[i]
        phone.contact_id = contact.contact_id
        phone.phone_type = phone_type_list[i]
        phone.area_code = area_code_list[i]
        phone.number = number_list[i]
        phone.save()
    date_id_list = request.POST.getlist('date_id')
    date_type_list = request.POST.getlist('date_type')
    date_list = request.POST.getlist('date')
    for i in range(len(date_type_list)):
        date = Date()
        if i < len(date_id_list):
            date.date_id = date_id_list[i]
        date.contact_id = contact.contact_id
        date.date_type = date_type_list[i]
        date.date = parse_date(date_list[i])
        date.save()
    return redirect('/')

def delete(request):
    contact_id = request.POST['contact_id']
    Contact.objects.get(contact_id=contact_id).delete()
    Address.objects.filter(contact_id=contact_id).delete()
    PhoneNumber.objects.filter(contact_id=contact_id).delete()
    Date.objects.filter(contact_id=contact_id).delete()
    return redirect('/')

def searchRecords(searchString=None):
    searchContactIdList = []
    searchWordList = searchString.split(" ")
    first = True
    for searchWord in searchWordList:
        resultContactIdList = []
        contactIdList = Contact.objects.values_list('contact_id', flat=True).annotate(search = SearchVector('fname', 'mname', 'lname'))\
            .filter(search=SearchQuery(searchWord)).order_by('contact_id')
        addressContactIdList = Address.objects.values_list('contact_id', flat=True).annotate(search=SearchVector('address_type', 'address', 'city','state', 'zip')) \
            .filter(search=SearchQuery(searchWord))
        phoneContactIdList = PhoneNumber.objects.values_list('contact_id', flat=True).annotate(search=SearchVector('phone_type', 'area_code', 'number')) \
            .filter(search=SearchQuery(searchWord))
        dateContactIdList = Date.objects.values_list('contact_id', flat=True).annotate(search=SearchVector('date_type', 'date')) \
            .filter(search=SearchQuery(searchWord))
        for contactId in contactIdList:
            resultContactIdList.append(contactId)
        for contactId in addressContactIdList:
            resultContactIdList.append(contactId)
        for contactId in phoneContactIdList:
            resultContactIdList.append(contactId)
        for contactId in dateContactIdList:
            resultContactIdList.append(contactId)
        if first:
            searchContactIdList = resultContactIdList
            first = False
        else:
            searchContactIdList = list(set(searchContactIdList) & set(resultContactIdList))
    resultContactIdList = list(set(searchContactIdList))
    contactList = Contact.objects.filter(contact_id__in=resultContactIdList).distinct()
    return contactList

def importdata():
    with open("E:/2.SPRING 2020/CS 6360.003 - Database Design(Dr. Chris Davis)/Projects/Project 1/Contacts.csv") as csvfile:
        recordList = csv.reader(csvfile, delimiter=',')
        a = False
        for record in recordList:
            if a:
                contact = Contact()
                contact.contact_id = record[0]
                contact.fname = record[1]
                contact.mname = record[2]
                contact.lname = record[3]
                contact.save()
                # breakpoint()
                if record[4] != '':
                    home_phone = PhoneNumber()
                    home_phone.contact_id = record[0]
                    home_phone.phone_type = 'Home'
                    home_phone.area_code = str(record[4][0]) + str(record[4][1]) + str(record[4][2])
                    home_phone.number = record[4][4] + record[4][5] + record[4][6] + record[4][8] + record[4][9] + record[4][10] + record[4][11]
                    home_phone.save()
                if record[5] != '':
                    cell_phone = PhoneNumber()
                    cell_phone.contact_id = record[0]
                    cell_phone.phone_type = 'Cell Phone'
                    cell_phone.area_code = record[5][0] + record[5][1] + record[5][2]
                    cell_phone.number = record[5][4] + record[5][5] + record[5][6] + record[5][8] + record[5][9] + record[5][10] + record[5][11]
                    cell_phone.save()
                if record[6] != '':
                    home_address = Address()
                    home_address.contact_id = record[0]
                    home_address.address_type = 'Home'
                    home_address.address = record[6]
                    home_address.city = record[7]
                    home_address.state = record[8]
                    home_address.zip = record[9]
                    home_address.save()
                if record[10] != '':
                    work_phone = PhoneNumber()
                    work_phone.contact_id = record[0]
                    work_phone.phone_type = 'Work Phone'
                    work_phone.area_code = record[10][0] + record[10][1] + record[10][2]
                    work_phone.number = record[10][4] + record[10][5] + record[10][6] + record[10][8] + record[10][9] + record[10][10] + record[10][11]
                    work_phone.save()
                if record[11] != '':
                    work_address = Address()
                    work_address.contact_id = record[0]
                    work_address.address_type = 'Work'
                    work_address.address = record[11]
                    work_address.city = record[12]
                    work_address.state = record[13]
                    work_address.zip = record[14]
                    work_address.save()
                if record[15] != '':
                    birth_date = Date()
                    birth_date.contact_id = record[0]
                    birth_date.date_type = 'Birthday'
                    birth_date.date = record[15]
                    birth_date.save()
                # if record[0] == '2':
                #     breakpoint()
            else:
                a = True