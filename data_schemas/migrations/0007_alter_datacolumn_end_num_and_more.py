# Generated by Django 4.1.7 on 2023-03-20 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_schemas', '0006_alter_datacolumn_end_num_alter_datacolumn_start_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacolumn',
            name='end_num',
            field=models.PositiveIntegerField(blank=True, default=10, null=True),
        ),
        migrations.AlterField(
            model_name='datacolumn',
            name='sentences_num',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='datacolumn',
            name='start_num',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='num_of_records',
            field=models.PositiveIntegerField(default=1),
        ),
    ]