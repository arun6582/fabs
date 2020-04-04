from fabric import task
from pathlib import Path
from fabs.ubuntu import base
import time


@task
def add_user(c, username, ssh_key_file=None):
    # this is performed by root account usually so sudo not required
    if(not ssh_key_file):
        home = str(Path.home())
        ssh_key_file = home + '/.ssh/id_rsa.pub'

    with open(ssh_key_file) as fd:
        ssh_key = fd.readline().strip()
    c.sudo("useradd -m %s" % username)
    c.sudo("usermod -s /bin/bash %s" % username)
    authorized_keys = "authorized_keys"
    base.append(c, "/etc/sudoers", "%s ALL=(ALL) NOPASSWD:ALL" % username, sudo=True)
    with c.cd("/home/%s" % username):
        c.run("sudo chmod go-w .")
        c.run("sudo mkdir .ssh")
        c.run("sudo chmod 700 .ssh")
        c.run("sudo touch .ssh/%s" % (authorized_keys))
        c.run("sudo chown %s:%s .ssh" % (username, username))
        c.run("sudo chown %s:%s .ssh/%s" % (username, username, authorized_keys))
        c.run('sudo chmod 644 .ssh/%s' % authorized_keys)
        base.append(c, ".ssh/%s" % authorized_keys, ssh_key, sudo=True)
        c.run("sudo service ssh restart")


@task
def delete_user(c, username):
    c.run('userdel -r %s' % username)


@task
def add_ssh_key(c, ssh_key_file=None):
    if(not ssh_key_file):
        home = str(Path.home())
        ssh_key_file = home + '/.ssh/id_rsa.pub'

    username = c.user
    with open(ssh_key_file) as fd:
        ssh_key = fd.readline().strip()
    authorized_keys = "authorized_keys"
    with c.cd("/home/%s" % username):
        base.append(c, ".ssh/%s" % authorized_keys, ssh_key)


@task
def upload_known_hosts(c):
    home = str(Path.home())
    file_path = home + '/.ssh/known_hosts'
    with open(file_path) as _f:
        content = _f.read()
        base.append(c, '/home/%s/.ssh/known_hosts' % c.user, content)


@task
def bash(c):
    local_home = str(Path.home())
    with c.cd("/home/%s" % c.user):
        c.put(local_home + '/.inputrc', "")
        c.put(local_home + '/.screenrc', "")
    c.run("sudo apt-get -y update")
    c.run("sudo apt-get -y install openssh-client openssh-server")


@task
def systemd(c, action, file_path, wait_before_restart=0, dest_filename=None, dest_file_prefix=None, template_context=None, sudo=True):

    def _filename(x):
        if(dest_file_prefix):
            return "%s%s" % (dest_file_prefix, x)
        return x

    dest_dir = "/etc/systemd/system"
    if(dest_filename):
        filename = _filename(dest_filename)
        destination_path = "%s/%s" % (dest_dir, filename)
    else:
        filename = _filename(file_path.split('/')[-1])
        destination_path = "%s/%s" % (dest_dir, filename)

    def _config():
        base.write_template(
            c,
            file_path,
            dest_file_prefix=dest_file_prefix,
            destination_path=destination_path,
            template_context=template_context,
            sudo=sudo
        )

    if(action == "start"):
        _config()
        c.sudo("systemctl daemon-reload")
        c.sudo("systemctl enable %s" % filename)
        c.sudo("systemctl start %s" % filename)
        time.sleep(wait_before_restart)
    elif(action == "restart"):
        c.sudo("systemctl stop %s" % filename)
        time.sleep(wait_before_restart)
        _config()
        c.sudo("systemctl daemon-reload")
        c.sudo("systemctl start %s" % filename)
        time.sleep(wait_before_restart)
    elif(action == "stop"):
        c.sudo("systemctl stop %s" % filename)
        c.sudo("systemctl disable %s" % filename)
        c.sudo("systemctl daemon-reload")
    return filename, destination_path


@task
def cron(c, action, minute, hour, day_month, month, day_week, cmd, remove_regex=None):
    if(action == '+'):
        c.run(
            'crontab -l | awk NF | { cat; echo -e "%s %s %s %s %s %s >> /tmp/cron.log 2>&1\n"; } | crontab -' % (
                minute,
                hour,
                day_month,
                month,
                day_week,
                cmd
            )
        )
    elif (action == '-'):
        assert remove_regex is not None
        c.run("crontab -l | grep -v '%s' | crontab -" % remove_regex)
    c.run('crontab -l')
