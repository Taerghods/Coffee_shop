# Generated by Django 4.2 on 2025-01-17 13:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_shop', '0005_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='رمز عبور باید حداقل ۸ کاراکتر و ترکیبی از حروف، اعداد و کاراکترهای خاص باشد.', max_length=100, validators=[django.core.validators.MinLengthValidator(9, message='رمز عبور باید حداقل ۸ کاراکتر باشد.'), django.core.validators.RegexValidator(message='رمز عبور باید حداقل شامل یک حرف کوچک، یک حرف بزرگ، یک عدد و یک کاراکتر خاص باشد.', regex='/^(?=.*\\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\\w\\d\\s:])([^\\s]){8,16}$')]),
        ),
    ]