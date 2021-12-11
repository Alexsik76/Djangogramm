# Generated by Django 4.0 on 2021-12-11 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_by_email', '0005_auto_20211209_2046'),
        ('gramm_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='liked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='gramm_app.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='liker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to='auth_by_email.djgrammuser'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('liked', 'liker'), name='unique_like'),
        ),
    ]
