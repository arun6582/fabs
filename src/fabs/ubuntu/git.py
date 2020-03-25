from fabric import task
from fabs.ubuntu import base


@task
def clone(c, git_dir, git_url, purge=False):
    if(purge):
        c.run("rm -rf %s" % git_dir)
    base.mkdir(c, git_dir)
    c.run("git clone %s %s" % (git_url, git_dir))


@task
def pull(c, git_dir):
    with c.cd(git_dir):
        c.run("git pull origin master")
