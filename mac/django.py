from invoke import task
from fabs.mac import base


@task
def collect_static(c, project_path, env_vars=None):
    if env_vars is None:
        env_vars = {}
    with base.virtualenv(c, project_path):
        with c.prefix(base.env_prefix(env_vars)):
            c.run("%s/manage.py collectstatic --noinput" % project_path)
