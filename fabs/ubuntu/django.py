from fabric import task
from fabs.ubuntu import base


@task
def collectstatic(c, project_path, settings_file=None, env_vars=None):
    if(settings_file):
        settings = " --settings %s" % settings_file
    else:
        settings = ""
    with base.virtualenv(c, project_path), c.cd(project_path):
        c.run("%s ./manage.py collectstatic --noinput%s" % (base.env_prefix(env_vars), settings))


@task
def migrate(c, project_path, settings_file=None, env_vars=None):

    if(settings_file):
        settings = " --settings %s" % settings_file
    else:
        settings = ""
    with base.virtualenv(c, project_path), c.cd(project_path):
        c.run("%s ./manage.py migrate%s" % (base.env_prefix(env_vars), settings))
