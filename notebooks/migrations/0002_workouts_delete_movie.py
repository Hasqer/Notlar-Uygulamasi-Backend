# Generated by Django 4.2.1 on 2023-06-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('notebooks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notebooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]
