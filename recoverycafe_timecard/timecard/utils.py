from django.db import connection


def get_report_data():
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM timecard_punchtime;'
        cursor.execute(sql)

        data = [row for row in cursor.fetchall()]

    return data