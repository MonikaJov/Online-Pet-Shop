# Generated by Django 4.2.1 on 2023-06-28 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pet_shop', '0015_cart_userprofile_cartproduct_userprofile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='userprofile',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='userprofile',
        ),
        migrations.RemoveField(
            model_name='order',
            name='userprofile',
        ),
        migrations.RemoveField(
            model_name='orderedproducts',
            name='userprofile',
        ),
        migrations.RemoveField(
            model_name='superuser',
            name='userprofile',
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderedproducts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='superuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
