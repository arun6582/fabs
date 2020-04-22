from fabs.mac import base
from invoke import task
from pathlib import Path
home = str(Path.home())


@task
def install_brew(c):
    c.run('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')


@task
def install_necessary_packages(c):
    c.run("brew install the_silver_searcher")
    c.run("brew install gnu-sed")
    c.run("brew install grep")
    c.run("pip3 install b2")


@task
def nginx(c):
    c.run("cp %s/root_nginx.conf /usr/local/etc/nginx/nginx.conf" % (base.root_templates))
    c.run("nginx -s reload")


@task
def git_prompt(c):
    c.run("rm -rf %s/.bash/git-aware-prompt" % home)
    base.mkdir(c, '%s/.bash' % home)
    c.run('git clone git://github.com/jimeh/git-aware-prompt.git %s/.bash/git-aware-prompt' % home)
    c.run("cat %s/prompt.sh >> %s/.bash/git-aware-prompt/prompt.sh" % (base.root_templates, home))


@task
def go_install(c):
    go_tar = '/tmp/go.tar.gz'
    c.run('wget -O %s https://dl.google.com/go/go1.14.2.darwin-amd64.tar.gz' % go_tar)
    c.sudo('tar -C /usr/local -xzf %s' % go_tar)

    go = '/usr/local/go/bin/go'
    print('Executable: %(go)s' % {'go': go})

    base.write_template(
        c,
        file_path="%s/hello.go" % base.root_templates,
        destination_path="/tmp/"
    )
    with c.cd('/tmp/'):
        c.run('%s build hello.go' % go)
        c.run('./hello')
