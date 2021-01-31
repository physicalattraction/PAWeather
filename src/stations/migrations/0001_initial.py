# Generated by Django 2.2.14 on 2021-01-31 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('code', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('longitude', models.DecimalField(decimal_places=3, max_digits=6)),
                ('latitude', models.DecimalField(decimal_places=3, max_digits=6)),
                ('altitude', models.DecimalField(decimal_places=3, max_digits=6)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
    ]
