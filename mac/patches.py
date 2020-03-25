import os
from invoke import task
import system
import base
import packages
from pathlib import Path
home = str(Path.home())


@task
def proxy(c, action, port, user, host, network):
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
            'port': port,
            'user': user,
            'logfile': '/tmp/proxy.log'
        }
    )
    if(action == 'start'):
        c.run('networksetup -setsocksfirewallproxy %s localhost %s' % (network, port))
        c.run('networksetup -setsocksfirewallproxystate %s on' % network)
    elif(action == 'stop'):
        c.run('networksetup -setsocksfirewallproxystate %s off' % network)

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
def find_and_replace(c, find, replace):
    c.run("ag %s -l |xargs -I {} gsed -i -E 's/%s/%s/' {}" % (find, find, replace))


@task
def find_and_replace_filenames(c, find, replace):
    c.run("ag -g %s |xargs -I {} sh -c \'result=\"{}\"; mv {} \"${result/%s/%s}\"\'" % (find, find, replace))


@task
def somaxconn(c, maxconn):
    c.sudo("sysctl kern.ipc.somaxconn=%s" % maxconn)


@task
def bash_common(c):
    c.run("cp %s/.bash_common.sh %s/" % (base.root_templates, home))


@task
def b2_delete(c, bucket, prefix, file_regex=None):
    if(file_regex):
        return c.run("b2 ls --recursive --long --versions %s %s | grep %s | while read c1 x x x x c6; do b2 delete-file-version $c6 $c1; done" % (
            bucket, prefix, file_regex
        ))
    c.run("b2 ls --recursive --long --versions %s %s | while read c1 x x x x c6; do b2 delete-file-version $c6 $c1; done" % (bucket, prefix))


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
    c.run("git clone git://github.com/ajh17/VimCompletesMe.git %s/.vim/pack/vendor/start/VimCompletesMe" % home)
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
