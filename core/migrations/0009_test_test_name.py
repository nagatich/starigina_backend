# Generated by Django 2.2.3 on 2019-09-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Название теста'),
        ),
    ]
