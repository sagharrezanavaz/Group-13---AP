# Generated by Django 4.2.13 on 2024-06-24 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Products'},
        ),
        migrations.RemoveField(
            model_name='cart',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='category',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='category',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='category',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='product',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='product',
            name='detail_description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated_at',
        ),
    ]
