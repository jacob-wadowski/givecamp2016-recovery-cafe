from .odsreader import ODSReader

KEYS = ('is_active', 'staff_id', '_staff_name')

def has_keys(row):
    return all([k in row for k in KEYS])

def find_records(data):
    records = []
    collecting = False
    indices = None

    for row in data:
        if collecting:
            if not any(row):
                break
            values = [row[i] for i in indices]
            if not all(values):
                break
            records.append({
                "active": True if values[0]=='t' else False,
                "staff_id": int(values[1]),
                'first_name': '',
                'last_name': values[2]
            })
        elif has_keys(row):
            indices = [row.index(k) for k in KEYS]
            collecting = True

    return records

def read_data(file_name, file):
    if file_name.endswith('.ods'):
        ods = ODSReader(file)
        return ods.SHEETS['Sheet1']
    else:
        return []

def get_volunteer_records(file_name, file):
    data = read_data(file_name, file)
    records = find_records(data)
    return records
