# Generated by Django 3.1.4 on 2021-01-01 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pwdgen', '0003_remove_category_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='password',
            options={'get_latest_by': '-created', 'ordering': ['-created'], 'verbose_name': 'Password', 'verbose_name_plural': 'Passwords'},
        ),
    ]