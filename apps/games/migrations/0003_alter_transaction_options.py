# Generated by Django 4.2.4 on 2023-09-19 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('-datetime_created',), 'verbose_name': 'Транзакция', 'verbose_name_plural': 'Транзакции'},
        ),
    ]
