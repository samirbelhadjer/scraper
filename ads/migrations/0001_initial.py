# Generated by Django 4.1.5 on 2023-01-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField()),
                ('photo', models.ImageField(upload_to='ad/')),
                ('title', models.CharField(max_length=255)),
                ('position', models.CharField(choices=[('Top', 'top'), ('Side', 'side')], max_length=4)),
            ],
        ),
    ]
