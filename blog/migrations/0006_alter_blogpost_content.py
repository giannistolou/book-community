# Generated by Django 5.1.3 on 2025-02-27 19:26

import prose.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blogpost_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=prose.fields.RichTextField(blank=True, null=True),
        ),
    ]
