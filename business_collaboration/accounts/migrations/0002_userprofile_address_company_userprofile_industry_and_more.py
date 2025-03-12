# Generated by Django 5.1.4 on 2025-03-12 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address_company',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='industry',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name_company',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='registration_number_company',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
