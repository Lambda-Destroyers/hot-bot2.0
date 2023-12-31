# Generated by Django 4.2 on 2023-08-17 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotbot_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('currency', models.CharField(max_length=50)),
                ('bot_run_time', models.IntegerField()),
                ('desired_ROI', models.DecimalField(decimal_places=10, max_digits=20)),
                ('stop_loss', models.DecimalField(decimal_places=10, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
