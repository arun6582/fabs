from invoke import task
import time
from pathlib import Path
home = str(Path.home())
from fabs.mac import base


@task
def hosts(c, action, host):
    if(action == '+'):
        base.append(c, '/etc/hosts', '127.0.0.1 %s' % host, sudo=True)
    elif(action == '-'):
        base.remove_line(c, "/etc/hosts", host, sudo=True)


@task
def launchctl(c, action, label, file_path, wait_before_restart=0, dest_filename=None, dest_file_prefix=None, template_context=None):

    def _filename(x):
        if(dest_file_prefix):
            return "%s_%s" % (dest_file_prefix, x)
        return x


    if(dest_filename):
        destination_path = "%s/%s/%s" % (home, 'Library/LaunchAgents', _filename(dest_filename)) 
    else:
        filename = file_path.split('/')[-1]
        destination_path = "%s/%s/%s" % (home, 'Library/LaunchAgents', _filename(filename)) 

    template_context['label'] = label
    file_address = base.write_template(c, file_path, destination_path=destination_path, template_context=template_context, sudo=False)
    if(action == 'start'):
        c.run("launchctl unload %s" % file_address)
        c.run("launchctl load -w %s" % file_address)
        c.run("launchctl start %s" % label)
    elif(action == 'stop'):
        c.run("launchctl stop %s" % label)
        c.run("launchctl unload %s" % file_address)
        c.run("rm -rf %s" % file_address)
    elif(action == 'restart'):
        c.run("launchctl stop %s" % label)
        time.sleep(wait_before_restart)
        c.run("launchctl start %s" % label)
    elif(action == 'reload'):
        c.run("launchctl unload %s" % file_address)
        c.run("launchctl load %s" % file_address)


@task
def cron(c, action, minute, hour, day_month, month, day_week, cmd, remove_regex=None):
    if(action == '+'):
        c.run(
            "crontab -l | { cat; echo '%s %s %s %s %s %s'; } | crontab -" % (
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
