from jinja2 import Template
from fabric import task
from contextlib import contextmanager
import uuid
import os


self_dir_path = os.path.dirname(os.path.realpath(__file__))
root_templates = "%s/templates/root" % self_dir_path


@task
def mkdir(c, path, sudo=False):
    cmd = "mkdir -p '%s'" % path
    if(sudo):
        c.sudo(cmd)
    c.run(cmd)


@task
def write_file(c, path, content, sudo=False):
    temp_file = '/tmp/%s' % uuid.uuid4().hex
    with open(temp_file, 'w') as f:
        f.write(content)
    if not sudo:
        c.put(temp_file, path)
    else:
        c.put(temp_file, temp_file)
        c.sudo('mv %s %s' % (temp_file, path))
    os.remove(temp_file)


@task
def append(c, path, content, sudo=False, replace_if=None):
    # supports single line append only
    # if replace_if is present it will replace the replace_if with content
    if replace_if:
        result = c.run('if grep -q %s %s; then echo yes; else echo no; fi' % (replace_if, path)).stdout.strip()
        if result == 'yes':
            c.run("sed 's/%s/%s/g' %s" % (replace_if, content, path))
            return
    if(sudo):
        return c.run("echo '%s' | sudo tee -a '%s'" % (content, path))
    c.run("echo '%s' | tee -a '%s'" % (content, path))


@task
def remove_line(c, path, line, sudo=True):
    cmd = "sed -i.bak '/%s/d' %s" % (line, path)
    if(sudo):
        return c.sudo(cmd)
    c.run(cmd)


@task
def timezone(c, timezone="Asia/Kolkata"):
    c.sudo("timedatectl set-timezone %s" % timezone)


@contextmanager
def virtualenv(c, path, env_name='env'):
    activate = 'source %s/%s/bin/activate' % (path, env_name)
    with c.prefix(activate):
        yield


def env_prefix(env=None):
    env = env or {'dummy': 1}
    return ' '.join(["""%s='%s'""" % (i[0], i[1]) for i in env.items()])


@task
def yarn_build(c, path, env=None):
    with c.cd(path):
        c.run("yarn; %s yarn build" % env_prefix(env))


@task
def npm_build(c, path):
    with c.cd(path):
        c.run("npm install; npm build")


@task
def venv(c, env_dir, env_name='env', purge=False, no_cache=False):
    if(purge):
        c.run("rm -rf %s/%s" % (env_dir, env_name))
    with c.cd(env_dir):
        c.run("python3.7 -m venv %s" % env_name)
    with virtualenv(c, env_dir, env_name):
        c.run("pip install wheel")
        if(no_cache):
            c.run("pip install -r %s/requirements.txt --no-cache-dir" % env_dir)
        else:
            c.run("pip install -r %s/requirements.txt" % env_dir)


@task
def write_template(c, file_path, destination_path=None, return_str=False, dest_file_prefix=None, template_context=None, sudo=False):
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
