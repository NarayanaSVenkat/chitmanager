#file for oracle db migration
from __future__ import with_statement
from fabric.api import *
import os, sys, imp, re; 
APP_ROOT = os.path.join(os.path.dirname(__file__), os.path.pardir)
sys.path += [APP_ROOT, os.path.join(APP_ROOT, 'lib')]
from support import config, get_db_handler

def list():
  migrations = [
    file for file in os.listdir('.') 
    if re.match('\d{4}-\d{2}-\d{2}.*(py|sql)$', file)
  ]
  print('Migrations in descending order:')
  print('') 
  for migration in sorted(migrations)[::-1]:
    print(' - %s' % migration)
  
def migrate(migration):
  filepath, extension = os.path.splitext(migration)
  if extension == '.py':
    migration = load_source('migration', os.path.join(APP_ROOT, 'migrations', migration))
    migration.migrate(get_db_handler(config['db']))
  elif extension == '.sql':
    local('mysql -u root -p %s < %s' % (
        config.db.database,
        os.path.join(APP_ROOT, 'migrations', migration)
      )
    )
