from django.db import connection


def get_report_data(start_date=None, end_date=None):
    with connection.cursor() as cursor:
        sql = '''SELECT * FROM timecard_punchtime 
                 WHERE punch_time >= {0}
                 AND punch_time <= {1};
              '''.format(start_date, end_date)
        cursor.execute(sql)

        data = [row for row in cursor.fetchall()]

    return data