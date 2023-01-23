# Generated by Django 3.2.1 on 2022-12-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolbot', '0004_alter_order_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_amount',
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_tasks_add',
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_tasks_arbitration',
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_tasks_arbitration_incorrect',
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_tasks_not_paid',
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_tasks_paid',
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_tasks_pass',
        ),
        migrations.RemoveField(
            model_name='student',
            name='stud_tasks_solved',
        ),
        migrations.RemoveField(
            model_name='student',
            name='tasks_arbitration_correctstud',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='tasks_arbitration_correctteach',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_amount',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_comission',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_fee',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_tasks_arbitration',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_tasks_arbitration_incorrect',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_tasks_not_paid',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_tasks_not_solved_in_time',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_tasks_paid',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_tasks_pass',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_tasks_solved',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teach_total_sum_to_pay',
        ),
        migrations.AddField(
            model_name='student',
            name='pay_number',
            field=models.CharField(default=1, max_length=300, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='pay_number',
            field=models.CharField(default=1, max_length=300, unique=True),
            preserve_default=False,
        ),
    ]
