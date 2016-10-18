import subprocess

subprocess.call(['./manage.py', 'migrate'])
subprocess.call(['./manage.py', 'buildinitialfixture'])
subprocess.call(['./manage.py', 'loaddata', 'timecard/fixtures/initialdatatemplate.json'])