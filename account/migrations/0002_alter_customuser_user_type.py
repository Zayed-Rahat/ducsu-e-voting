# Generated by Django 4.2.3 on 2023-09-24 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('voter', 'Voter')], default=2, max_length=6),
        ),
    ]
