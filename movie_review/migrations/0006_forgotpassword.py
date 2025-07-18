# Generated by Django 5.2 on 2025-05-20 15:55

import django.db.models.deletion
import movie_review.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_review', '0005_search'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgotPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(default=movie_review.utils.default_time_plus_10)),
                ('is_used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forgot_password_user_id', to='movie_review.users')),
            ],
        ),
    ]
