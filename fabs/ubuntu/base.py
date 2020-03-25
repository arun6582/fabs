from jinja2 import Template
from fabric import task
from contextlib import contextmanager
import uuid


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


@task
def append(c, path, content, sudo=False):
    if(sudo):
        return c.sudo("echo '%s' | sudo tee -a '%s'" % (content, path))
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
    return ' '.join(['='.join([str(j) for j in i]) for i in env.items()])


@task
def yarn_build(c, path):
    with c.cd(path):
        c.run("yarn; yarn build")


@task
def venv(c, env_dir, env_name='env', purge=False):
    if(purge):
        c.run("rm -rf %s/%s" % (env_dir, env_name))
    with c.cd(env_dir):
        c.run("python3.7 -m venv %s" % env_name)
    with virtualenv(c, env_dir, env_name):
        c.run("pip install wheel")
        c.run("pip install -r %s/requirements.txt" % env_dir)


@task
def free_space(c):
    c.run("df -h")


@task
def write_template(c, file_path, destination_path=None, return_str=False, dest_name_prefix=None, template_context=None, sudo=False):
    with open(file_path) as f:
        template = Template(f.read())

    template_context = template_context or {}
    output = template.render(template_context)
    if(return_str):
        return output
    if(dest_name_prefix):
        filename = "%s_%s" % (dest_name_prefix, file_path.split('/')[-1])
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