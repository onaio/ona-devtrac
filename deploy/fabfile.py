import os
import sys

from fabric.api import env, run, cd, lcd, sudo, put
from fabric.contrib import files


DEPLOYMENTS = {
    'default': {
        'home': '/var/www',
        'host_string':
        'ubuntu@stage.ona.io',
        'project': 'devtrac',
        'key_filename': os.path.expanduser('~/.ssh/ona.pem'),
        'django_module': 'devtrac.preset.local_settings'
    },
}

current_working_dir = os.path.dirname(__file__)


def run_in_virtualenv(command):
    d = {
        'activate': os.path.join(
            env.virtualenv, env.project, 'bin', 'activate'),
        'command': command,
    }
    run('source %(activate)s && %(command)s' % d)


def check_key_filename(deployment_name):
    if 'key_filename' in DEPLOYMENTS[deployment_name] and \
       not os.path.exists(DEPLOYMENTS[deployment_name]['key_filename']):
        print("Cannot find required permissions file: %s" %
              DEPLOYMENTS[deployment_name]['key_filename'])

        return False

    return True


def setup_env(deployment_name):
    env.update(DEPLOYMENTS[deployment_name])

    if not check_key_filename(deployment_name):
        sys.exit(1)

    env.code_src = os.path.join(env.home, env.project)
    env.virtualenv = os.path.join(env.home, '.virtualenvs')


def change_local_settings(config_module, dbname, dbuser, dbpass,
                          dbhost='127.0.0.1'):
    config_path = os.path.join(
        env.code_src, config_module.replace('.', '/') + '.py')
    if files.exists(config_path):
        files.sed(config_path, 'REPLACE_DB_NAME', dbname)
        files.sed(config_path, 'REPLACE_DB_USER', dbuser)
        files.sed(config_path, 'REPLACE_DB_PASSWORD', dbpass)
        files.sed(config_path, 'REPLACE_DB_HOST', dbhost)


def system_setup(deployment_name, dbuser='dbuser', dbpass="dbpwd"):
    setup_env(deployment_name)
    sudo('sh -c \'echo "deb http://apt.postgresql.org/pub/repos/apt/ '
         'precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list\'')
    sudo('wget --quiet -O - http://apt.postgresql.org/pub'
         '/repos/apt/ACCC4CF8.asc | apt-key add -')
    sudo('apt-get update')
    sudo('apt-get install -y nginx git python-setuptools python-dev binutils'
         ' libproj-dev gdal-bin Postgresql-9.3-postgis libpq-dev')
    sudo('easy_install pip')
    sudo('pip install virtualenvwrapper uwsgi')

    run('sudo -u postgres psql -U postgres -d postgres'
        ' -c "CREATE USER %s with password \'%s\';"' % (dbuser, dbpass))
    run('sudo -u postgres psql -U postgres -d postgres'
        ' -c "CREATE DATABASE %s OWNER %s;"' % (dbuser, dbuser))


def server_setup(deployment_name, dbuser='dbuser', dbpass="dbpwd"):
    # system_setup(deployment_name, dbuser, dbpass)
    setup_env(deployment_name)

    sudo('mkdir -p %s' % env.home)
    sudo('chown -R ubuntu %s' % env.home)

    with cd(env.home):
        run('git clone git@github.com:onaio/ona-devtrac.git devtrac'
            ' || (cd devtrac && git fetch && git checkout origin/master)')

    with lcd(current_working_dir):
        config_path = os.path.join(env.code_src, 'devtrac',
                                   'preset', 'local_settings.py')
        put(os.path.join('context', config_path[1:]), config_path)
        change_local_settings(env.django_module, dbuser, dbuser, dbpass)

        put('./etc/init/devtrac.conf', '/etc/init/devtrac.conf', use_sudo=True)
        put('./etc/nginx/sites-available/nginx.conf',
            '/etc/nginx/sites-available/devtrac.conf', use_sudo=True)
        sudo('(test -e /etc/nginx/sites-enabled/devtrac'
             ' && unlink /etc/nginx/sites-enabled/devtrac) || echo "no file"')
        sudo('ln -s /etc/nginx/sites-available/devtrac.conf'
             ' /etc/nginx/sites-enabled/devtrac')
    data = {
        'venv': env.virtualenv, 'project': env.project
    }
    run('WORKON_HOME=%(venv)s source /usr/local/bin/virtualenvwrapper.sh'
        ' && WORKON_HOME=%(venv)s mkvirtualenv %(project)s' % data)
    run('echo "export WORKON_HOME=%(venv)s" >> ~/.bashrc' % data)
    run('echo "export DJANGO_SETTINGS_MODULE=%s" >> ~/.bashrc'
        % env.django_module)

    with cd(os.path.join(env.home, env.project)):
        run_in_virtualenv('pip install -r requirements/common.pip')
        run_in_virtualenv("python manage.py syncdb --noinput --settings='%s'"
                          % env.django_module)
        run_in_virtualenv("python manage.py migrate --settings='%s'"
                          % env.django_module)
        run_in_virtualenv("python manage.py collectstatic --noinput"
                          " --settings='%s'" % env.django_module)

    sudo('/etc/init.d/nginx restart')
    sudo('mkdir -p /var/log/uwsgi')
    sudo('chown -R ubuntu /var/log/uwsgi')
    sudo('start devtrac')
