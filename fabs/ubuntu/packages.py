from fabric import task
from fabs.ubuntu import base

@task
def install_postgres_10(
            c,
            install=True,
            pg_hba=None,
            postgresql_conf=None
        ):
    if(install):
        c.run("wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -")
        c.run("""sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'""")
        c.run("sudo apt-get -y update")
        c.run("sudo apt-get install -y postgresql-10")
        c.run("sudo apt-get install -y libpq-dev")
    if(pg_hba):
        base.write_template(
            c,
            destination_path='/etc/postgresql/10/main/',
            **pg_hba
        )
    if(postgresql_conf):
        base.write_template(
            c,
            destination_path="/etc/postgresql/10/main/conf.d/",
            **postgresql_conf
        )
    c.run("sudo systemctl restart postgresql")


@task
def node_10(c):
    c.run("curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -")
    c.sudo("apt-get install -y nodejs")


@task
def go_install(c):
    go_tar = '/tmp/go.tar.gz'
    c.run('wget -O %s https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz' % go_tar)
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
