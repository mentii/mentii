import os
import sys
import site

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__),     'env/local/lib/python2.7/site-packages'))

# Path of execution
sys.path.append('/var/www/html/Backend')

#Add usr/local/bin
os.environ['PATH'] += ':/usr/local/bin'

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'env/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))

# import my_flask_app as application
from app import app as application
