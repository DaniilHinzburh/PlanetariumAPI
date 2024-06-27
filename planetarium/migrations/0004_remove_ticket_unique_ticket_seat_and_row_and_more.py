# Generated by Django 5.0.6 on 2024-06-16 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0003_remove_ticket_unique_ticket_seat_and_row_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ticket',
            name='unique_ticket_seat_and_row',
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('id', 'show_session', 'seat', 'row')},
        ),
    ]
