# Generated by Django 4.2 on 2023-04-21 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
