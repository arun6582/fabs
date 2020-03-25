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
