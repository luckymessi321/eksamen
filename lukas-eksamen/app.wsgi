import sys
import site
import os

site.addsitedir('/var/www/Semesteroppgave-2nd-periode/env/lib/python3.13/site-packages')

sys.path.insert(0, '/var/www/Semesteroppgave-2nd-periode')

os.chdir('/var/www/Semesteroppgave-2nd-periode')

os.environ['VIRTUAL_ENV'] = '/var/www/Semesteroppgave-2nd-periode/env'
os.environ['PATH'] = '/var/www/Semesteroppgave-2nd-periode/env/bin:' + os.environ['PATH']

from app import app as application