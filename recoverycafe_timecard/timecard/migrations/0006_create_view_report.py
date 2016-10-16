### script creates views

# DEPENDENCIES:
# db is created prior to running

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timecard', '0001_initial'),
        ('timecard', '0002_auto_20161015_2220'),
    ]

    operations = [
            migrations.RunSQL('DROP VIEW IF EXISTS view_report;'),
            migrations.RunSQL('''
                CREATE VIEW view_report AS
                
                SELECT
                    b.staff_id,
                    b.first_name,
                    b.last_name,
                    d.branch_name,
                    c.task_name,
                    a.punch_time_in,
                    a.punch_time_out,
                    ((CAST(strftime('%s',a.punch_time_out) AS float) - CAST(strftime('%s',a.punch_time_in) AS float)) / (60 * 60)) AS session_time_hours
                
                FROM (
                    SELECT
                        in_.volunteer_id_id,
                        in_.branch_id_id,
                        in_.task_id_id,
                        in_.punch_time AS punch_time_in,
                        min(out_.punch_time) AS punch_time_out
                    FROM timecard_punchtime AS in_
                    LEFT OUTER JOIN timecard_punchtime AS out_
                        ON in_.volunteer_id_id = out_.volunteer_id_id
                        AND in_.punch_time < out_.punch_time
                    WHERE in_.punch_type = "IN"
                        AND (out_.punch_type = "OUT" OR out_.punch_type IS NULL)
                    GROUP BY 
                        in_.volunteer_id_id,
                        in_.branch_id_id,
                        in_.task_id_id,
                        in_.punch_time
                ) a

                LEFT OUTER JOIN timecard_volunteer AS b
                    ON a.volunteer_id_id = b.id
                LEFT OUTER JOIN timecard_task AS c
                    ON a.task_id_id = c.id
                LEFT OUTER JOIN timecard_branch AS d
                    ON a.branch_id_id = d.id
                ;
                ''')
    ]
