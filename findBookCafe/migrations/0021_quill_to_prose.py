import json

import prose.fields
from django.db import migrations

QUILL_FIELDS = [
    ('Shop', 'description'),
    ('SimplePage', 'content'),
]


def quill_json_to_html(value):
    try:
        data = json.loads(value)
    except (TypeError, ValueError):
        return value
    if isinstance(data, dict) and 'html' in data:
        return data['html']
    return value


def html_to_quill_json(value):
    return json.dumps({'delta': '', 'html': value})


def convert(apps, converter):
    for model_name, field_name in QUILL_FIELDS:
        model = apps.get_model('findBookCafe', model_name)
        for pk, value in model.objects.values_list('pk', field_name):
            # update() instead of save() keeps updated_on untouched
            model.objects.filter(pk=pk).update(**{field_name: converter(value)})


def forwards(apps, schema_editor):
    convert(apps, quill_json_to_html)


def backwards(apps, schema_editor):
    convert(apps, html_to_quill_json)


class Migration(migrations.Migration):

    dependencies = [
        ('findBookCafe', '0020_alter_collection_options_alter_shop_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=prose.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='simplepage',
            name='content',
            field=prose.fields.RichTextField(),
        ),
        migrations.RunPython(forwards, backwards),
    ]
