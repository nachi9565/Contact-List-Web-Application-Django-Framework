# Generated by Django 3.0.4 on 2020-03-21 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact_id', models.IntegerField()),
                ('address_type', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=100)),
                ('mname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('date_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact_id', models.IntegerField()),
                ('date_type', models.CharField(max_length=100)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('phone_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact_id', models.IntegerField()),
                ('phone_type', models.CharField(max_length=100)),
                ('area_code', models.CharField(max_length=3)),
                ('number', models.CharField(max_length=7)),
            ],
        ),
    ]
