try: 
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import sys, os 
cwd = os.getcwd() 
sys.path.append(cwd) 
sys.path.append(cwd + '/radiatorSite') 
os.environ['DJANGO_SETTINGS_MODULE'] = "radiatorSite.settings" 
from django.core.wsgi import get_wsgi_application 
application = get_wsgi_application()
