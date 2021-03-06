# Generated by Django 3.1.5 on 2021-01-24 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('type', models.CharField(choices=[('Sell', 'Sell'), ('Rent', 'Rent'), ('Sell or Rent', 'Sell or Rent')], default='Sell', max_length=12)),
                ('price', models.IntegerField()),
                ('description', models.TextField(default='No Description Given')),
                ('image', models.ImageField(default='default.jpeg', upload_to='product')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoard.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(default=django.utils.timezone.now)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoard.customer')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoard.owner')),
                ('products', models.ManyToManyField(to='hoard.Product')),
            ],
        ),
    ]
