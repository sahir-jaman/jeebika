# Generated by Django 5.0.1 on 2024-01-30 18:45

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='service_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('company_exp', models.PositiveIntegerField(blank=True, null=True)),
                ('company_address', models.TextField(blank=True, null=True)),
                ('company_size', models.PositiveIntegerField(blank=True, null=True)),
                ('industry_type', models.CharField(blank=True, max_length=100, null=True)),
                ('business_desc', models.TextField(blank=True, null=True)),
                ('trade_number', models.PositiveIntegerField(blank=True, null=True)),
                ('rl_number', models.PositiveIntegerField(blank=True, null=True)),
                ('web_url', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='job_post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_title', models.CharField(blank=True, max_length=100, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('vacancy', models.PositiveIntegerField(blank=True, null=True)),
                ('published', models.DateField(blank=True, null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('skill', models.TextField(blank=True, null=True)),
                ('experience', models.TextField(blank=True, null=True)),
                ('requirements', models.TextField(blank=True, null=True)),
                ('responsibilities', models.TextField(blank=True, null=True)),
                ('expertise', models.CharField(blank=True, max_length=200, null=True)),
                ('employment_status', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('company_info', models.CharField(blank=True, max_length=100, null=True)),
                ('compensation', models.CharField(blank=True, max_length=100, null=True)),
                ('apply_procedure', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to='employees.category')),
                ('service_type', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to='employees.service_type')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
