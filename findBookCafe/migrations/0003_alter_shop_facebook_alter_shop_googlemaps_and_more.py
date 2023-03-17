# Generated by Django 4.0.6 on 2022-07-23 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findBookCafe', '0002_alter_shop_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='facebook',
            field=models.URLField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='shop',
            name='googleMaps',
            field=models.URLField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='shop',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='shop',
            name='instagram',
            field=models.URLField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='shop',
            name='tripadvisor',
            field=models.URLField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='shop',
            name='website',
            field=models.URLField(blank=True, max_length=300),
        ),
    ]
