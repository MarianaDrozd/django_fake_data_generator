# Generated by Django 4.1.7 on 2023-03-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_schemas', '0004_remove_dataset_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacolumn',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]
