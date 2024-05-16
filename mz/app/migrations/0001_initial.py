# Generated by Django 4.2.13 on 2024-05-15 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.IntegerField(unique=True)),
                ('order_type', models.CharField(choices=[('تنفيذ شبكة', 'Network'), ('عداد', 'Counter'), ('طوارئ', 'Emergency'), ('إحلال', 'Substitute'), ('التعزيز', 'Reinforcement'), ('الجهد المتوسط', 'Effort')], max_length=50)),
                ('employment_type', models.CharField(blank=True, max_length=40, null=True)),
                ('contractor_name', models.CharField(max_length=50)),
                ('distract', models.CharField(max_length=50)),
                ('materials', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=5)),
                ('month', models.CharField(max_length=5)),
                ('day', models.CharField(max_length=5)),
                ('safety_violations', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_img', models.ImageField(default='img/unknown.png', upload_to='address')),
                ('notes', models.TextField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
            ],
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultant_name', models.CharField(max_length=50)),
                ('job_number', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=13)),
                ('user_role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], max_length=10)),
                ('main_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usertable'),
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_img', models.ImageField(default='img/unknown.png', upload_to='object')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_img', models.ImageField(default='img/unknown.png', upload_to='address')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
            ],
        ),
    ]
