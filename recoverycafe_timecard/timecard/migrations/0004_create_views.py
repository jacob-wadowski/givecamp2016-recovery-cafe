### script creates views

# DEPENDENCIES:
# db is created prior to running

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timecard', '0001_initial'),
    ]

    operations = [
            migrations.RunSQL('DROP VIEW view_last_known_status;'),
            migrations.RunSQL('''
    CREATE VIEW view_last_known_status AS
    SELECT
        c.staff_id,
        c.first_name,
        c.last_name,
        a.punch_time_latest,
        b.punch_type AS punch_type_latest
    
    FROM (
        SELECT
            volunteer_id_id,
            MAX(punch_time) AS punch_time_latest
        FROM timecard_punchtime
        GROUP BY volunteer_id_id
    ) a
    LEFT OUTER JOIN timecard_punchtime AS b
        ON a.volunteer_id_id = b.volunteer_id_id
        AND a.punch_time_latest = b.punch_time
    LEFT OUTER JOIN timecard_volunteer AS c
        ON a.volunteer_id_id = c.id;
    ''')
    ]
