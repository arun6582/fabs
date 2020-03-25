import os
from invoke import task
from contextlib import contextmanager
from jinja2 import Template
import uuid

self_dir_path = os.path.dirname(os.path.realpath(__file__))
root_templates = "%s/templates/root" % self_dir_path


@task
def mkdir(c, path, sudo=False):
    cmd = "mkdir -p '%s'" % path
    if(sudo):
        return c.sudo(cmd)
    c.run(cmd)


@contextmanager
def virtualenv(c, project_path, env='env'):

    env_path = 'source %s/bin/activate' % env
    with c.cd(project_path):
        with c.prefix(env_path):
            yield


@task
def venv(c, project_path, env_name='env', purge=False):
    if(purge):
        c.run("rm -rf %s/%s" % (project_path, env_name))
    c.run("python3 -m venv %s" % env_name)
    with virtualenv(c, project_path, env_name):
        c.run("pip install -r %s/requirements.txt" % project_path)


def env_prefix(env):
    env['dummy'] = 1
    return " ".join(["%s=%s" % (i[0], i[1]) for i in env.items()])


@task
def yarn_build(c, path):
    with c.cd(path):
        c.run("yarn; yarn build")


@task
def append(c, path, content, sudo=False):
    if(sudo):
        return c.sudo('echo "%s" | sudo tee -a "%s"' % (content, path))
    c.run('echo "%s" | tee -a "%s"' % (content, path))


@task
def remove_line(c, path, regex, sudo=False):
    cmd = "sed -i '' '/%s/d' %s" % (regex, path)
    if(sudo):
        return c.sudo(cmd)
    c.run(cmd)


@task
def write_file(c, path, content, sudo=False):
    if not sudo:
        with open(path, 'w') as f:
            return f.write(content)
    temp_file = '/tmp/%s' % uuid.uuid4().hex
    with open(temp_file, 'wb') as f:
        f.write(content)
        c.sudo('mv %s %s' % (temp_file, path))


@task
def write_template(c, file_path, destination_path=None, dest_file_prefix=None, return_str=False, template_context=None, sudo=False):
    with open(file_path) as f:
        template = Template(f.read())

    template_context = template_context or {}
    output = template.render(template_context)
    if(return_str):
        return output
    if(dest_file_prefix):
        filename = "%s_%s" % (dest_file_prefix, file_path.split('/')[-1])
    else:
        filename = file_path.split('/')[-1]
    assert destination_path
    if(destination_path.endswith('/')):
        mkdir(c, destination_path, sudo=sudo)
        file_address = destination_path + filename
        write_file(c, file_address, output, sudo=sudo)
        return file_address
    else:
        folder = "/".join(destination_path.split('/')[:-1])
        mkdir(c, folder, sudo=sudo)
        write_file(c, destination_path, output, sudo=sudo)
        return destination_path

