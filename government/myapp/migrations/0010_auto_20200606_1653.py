# Generated by Django 3.0.5 on 2020-06-06 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20200605_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='linear_function',
            name='LDivisor',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='multiple_function',
            name='MDivisor',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
