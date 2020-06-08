# Generated by Django 3.0.4 on 2020-04-06 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_useric'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wage',
            options={'verbose_name_plural': '个人信息'},
        ),
        migrations.RenameField(
            model_name='wage',
            old_name='amount',
            new_name='pf',
        ),
        migrations.AddField(
            model_name='wage',
            name='ss',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
