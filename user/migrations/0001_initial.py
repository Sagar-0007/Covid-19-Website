# Generated by Django 2.0 on 2021-04-18 12:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminservice', '0002_auto_20210418_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billaddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.BigIntegerField()),
                ('pincode', models.IntegerField()),
                ('address', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/')),
                ('price', models.FloatField()),
                ('quantity', models.BigIntegerField()),
                ('prodid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminservice.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=20000)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(blank=True, default=None, max_length=100, null=True, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/')),
                ('price', models.FloatField()),
                ('quantity', models.BigIntegerField()),
                ('Payment_status', models.CharField(blank=True, max_length=20, null=True)),
                ('Datetime_of_payment', models.DateTimeField(default=django.utils.timezone.now)),
                ('Payment_mode', models.CharField(max_length=20)),
                ('Success_mode', models.CharField(max_length=20)),
                ('Invoice_No', models.BigIntegerField(default=0)),
                ('Razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('Razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('prodid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminservice.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardName', models.CharField(max_length=100)),
                ('cardNo', models.CharField(max_length=12)),
                ('expirationDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='User_feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Datetime_of_feedback', models.DateTimeField(default=django.utils.timezone.now)),
                ('feedback_message', models.TextField(max_length=10000)),
                ('prodid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminservice.Product')),
            ],
        ),
        migrations.CreateModel(
            name='User_register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=200)),
                ('user_contact', models.BigIntegerField()),

            ],
        ),
        migrations.AddField(
            model_name='user_feedback',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User_register'),
        ),
        migrations.AddField(
            model_name='payment',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User_register'),
        ),
        migrations.AddField(
            model_name='order',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User_register'),
        ),
        migrations.AddField(
            model_name='contact',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User_register'),
        ),
        migrations.AddField(
            model_name='cart',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User_register'),
        ),
        migrations.AddField(
            model_name='billaddress',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User_register'),
        ),
    ]
