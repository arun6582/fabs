import os
from invoke import task
from fabs.mac import system
from fabs.mac import base
from fabs.mac import packages
from pathlib import Path
home = str(Path.home())


@task
def proxy(c, action, local_port, host, network, remote_port=9836):
    if(action == '1'):
        action = 'start'
    elif action == '0':
        action = 'stop'

    system.launchctl(
        c,
        action,
        label='proxy.tunnel',
        wait_before_restart=0,
        file_path="%s/%s" % (base.root_templates, 'proxy.plist'),
        template_context={
            'host': host,
            'local_port': local_port,
            'remote_port': remote_port,
            'logfile': '/tmp/proxy.log'
        }
    )
    if(action == 'start'):
        c.run('networksetup -setsocksfirewallproxy %s localhost %s' % (network, local_port))
        c.run('networksetup -setsocksfirewallproxystate %s on' % network)
    elif(action == 'stop'):
        c.run('networksetup -setsocksfirewallproxystate %s off' % network)


@task
def port_forward(c, action, local_port, remote_port, user, host, ip='localhost'):
    if(action == '1'):
        action = 'start'
    elif action == '0':
        action = 'stop'

    system.launchctl(
        c,
        action,
        label='port.fordward.%s.tunnel' % local_port,
        wait_before_restart=0,
        file_path="%s/%s" % (base.root_templates, 'port_forwarding.plist'),
        dest_filename="port_forwarding_%s_%s.plist" % (local_port, remote_port),
        template_context={
            'host': host,
            'user': user,
            'local_port': local_port,
            'ip': ip,
            'remote_port': remote_port,
            'logfile': '/tmp/port_forwarding.log'
        }
    )


@task
def dotfiles(c, alias):
    # alias is namespace for files in git repo
    if (not os.path.isdir('%s/dotfiles/.git' % home)):
        with c.cd(home):
            c.run("git clone git@bitbucket.org:arun6582/dotfiles.git")
    base.write_template(
        c,
        file_path="%s/%s" % (base.root_templates, '.dotfiles.sh'),
        destination_path="%s/" % home,
        template_context={
            'alias': alias,
            'home': home
        }
    )
    cmd = "/bin/bash %s/.dotfiles.sh" % home
    c.run("crontab -l | { cat; echo '0 * * * * %s'; } | crontab -" % cmd)
    base.mkdir(c, "%s/bin" % home)
    c.run("cp %s/gcs %s/bin/" % (base.root_templates, home))


@task
def unload_plist(c, grep_regex, path):
    path = os.path.abspath(path)
    c.run(
        "ls %s | grep %s | xargs -I {} launchctl unload %s/{}" %
        (path, grep_regex, path)
    )
    c.run(
        "ls %s | grep %s | xargs -I {} rm -rf %s/{}" %
        (path, grep_regex, path)
    )


@task
def find_and_replace(c, find, replace, path=None):
    path = path or ''
    c.run("ag %s %s -l |xargs -I {} sh -c 'echo replacing in {}; gsed -i -E \"s/%s/%s/\" {}'" % (find, path, find, replace))


@task
def find_and_replace_filenames(c, find, replace, path=None):
    path = path or ''
    c.run("ag %s -g %s |xargs -I {} sh -c \'result=\"{}\"; new=\"${result/%s/%s}\"; echo $result renamed to $new; mkdir -p `dirname $new`; mv {} $new\'" % (path, find, find, replace))


@task
def somaxconn(c, maxconn):
    c.sudo("sysctl kern.ipc.somaxconn=%s" % maxconn)


@task
def bash_common(c):
    c.run("cp %s/.bash_common.sh %s/" % (base.root_templates, home))


@task
def b2_delete(c, bucket, prefix, file_regex=None):
    if(file_regex):
        return c.run("b2 ls --recursive --long --versions %s %s | grep %s | while read c1 x x x x c6; do b2 delete-file-version $c1; done" % (
            bucket, prefix, file_regex
        ))
    c.run("b2 ls --recursive --long --versions %s %s | while read c1 x x x x c6; do b2 delete-file-version $c1; done" % (bucket, prefix))


@task
def b2_size(c, bucket, prefix):
    c.run("b2 ls --long --versions --recursive %s %s | awk '{s+=$5} END {print s/1000/1000}MB'" % (bucket, prefix))


@task
def dock_lock(c, state):
    c.run("defaults write com.apple.dock contents-immutable -bool %s" % state)
    c.run("killall Dock")


@task
def dock_lock_size(c, state):
    c.run("defaults write com.apple.Dock size-immutable -bool %s" % state)
    c.run("killall Dock")


@task
def vim(c):
    c.run("cp %s/.vimrc %s/" % (base.root_templates, home))
    c.run("rm -rf %s/.vim" % home)
    c.run("git clone https://github.com/VundleVim/Vundle.vim.git %s/.vim/bundle/Vundle.vim" % home)
    c.run("vim +PluginInstall +qall")


@task
def new(c):
    packages.brew(c)
    packages.install_necessary_packages(c)
    vim(c)
    packages.git_prompt(c)
    bash_common(c)
    dotfiles(c)
    dock_lock(c)
    dock_lock_size(c)


@task
def setup_screenshot_format(c, screenshot_folder):
    base.mkdir(c, screenshot_folder)
    c.run('defaults write com.apple.screencapture location "%s"' % screenshot_folder)
    c.run('defaults write com.apple.screencapture name "Screenshot"')
    c.run('defaults write com.apple.screencapture "include-date" 1')
    c.run('killall SystemUIServer')


@task
def screenshot_uploader_imgur(c, action, img_client_id, img_secret_id, screenshot_folder):
    screenshot_folder = os.path.abspath(screenshot_folder)
    c.run('pip3 install imgur-uploader')
    setup_screenshot_format(c, screenshot_folder)
    script_path = base.write_template(
        c,
        file_path="%s/%s" % (base.root_templates, 'screenshot_uploader_imgur.sh'),
        destination_path=home + '/.screenshot_automation/'
    )
    imgur_python = c.run('which imgur-uploader').stdout.strip()
    gnu_grep = c.run('which ggrep').stdout.strip()
    envs = (
        ('IMGUR_API_ID', img_client_id),
        ('IMGUR_API_SECRET', img_secret_id),
        ('imguruploader', imgur_python),
        ('grep', gnu_grep)
    )
    system.launchctl(
        c,
        action,
        label='screenshot.uploader',
        wait_before_restart=0,
        file_path="%s/%s" % (base.root_templates, 'screenshot_watcher.plist'),
        template_context={
            'screen_shot_path': screenshot_folder,
            'logfile': '/tmp/screenshot.log',
            'path_to_script': script_path,
            'envs': envs
        }
    )


@task
def screenshot_uploader_b2(c, action, b2_client_id, b2_secret_id, bucket, screenshot_folder):
    screenshot_folder = os.path.abspath(screenshot_folder)
    c.run('pip3 install b2')
    setup_screenshot_format(c, screenshot_folder)
    script_path = base.write_template(
        c,
        file_path="%s/%s" % (base.root_templates, 'screenshot_uploader_b2.sh'),
        destination_path=home + '/.screenshot_automation/'
    )
    b2_python = c.run('which b2').stdout.strip()
    gnu_grep = c.run('which ggrep').stdout.strip()
    envs = (
        ('B2_APPLICATION_KEY_ID', b2_client_id),
        ('B2_APPLICATION_KEY', b2_secret_id),
        ('B2_BUCKET', bucket),
        ('B2_PATH', b2_python),
        ('GREP', gnu_grep),
        ('LC_ALL', 'en_US.UTF-8'),
        ('LANG', 'en_US.UTF-8'),
        ('LANGUAGE', 'en_US.UTF-8')
    )
    system.launchctl(
        c,
        action,
        label='screenshot.uploader',
        wait_before_restart=0,
        file_path="%s/%s" % (base.root_templates, 'screenshot_watcher.plist'),
        template_context={
            'screen_shot_path': screenshot_folder,
            'logfile': '/tmp/screenshot.log',
            'path_to_script': script_path,
            'envs': envs
        }
    )
