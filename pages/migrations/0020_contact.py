# Generated by Django 5.0.6 on 2024-06-17 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
            ],
        ),
    ]