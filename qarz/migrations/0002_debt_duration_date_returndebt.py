# Generated by Django 4.2.16 on 2024-11-17 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qarz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='debt',
            name='duration_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ReturnDebt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now=True)),
                ('debt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qarz.debt')),
            ],
        ),
    ]
