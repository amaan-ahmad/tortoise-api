# Generated by Django 4.0.6 on 2022-07-13 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0004_alter_promotion_plan'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='customergoals',
            constraint=models.UniqueConstraint(fields=('plan', 'user'), name='unique_enrollment'),
        ),
    ]
