from fabric import task
from fabs.ubuntu import base


@task
def b2_delete(c, bucket, prefix, file_regex=None, shell_env=None):
    shell_env = shell_env or {}
    if(file_regex):
        return c.run("b2 ls --recursive --long --versions %s %s | grep %s | while read c1 x x x x c6; do b2 delete-file-version $c6 $c1; done" % (
            bucket, prefix, file_regex
        ), env=shell_env)
    c.run("b2 ls --recursive --long --versions %s %s | while read c1 x x x x c6; do b2 delete-file-version $c6 $c1; done" % (bucket, prefix), env=shell_env)


@task
def setup_ikev2(c, username, password, vpn_name='MyVpn', ssh_port=22):
    template_folder = '%s/ikev2' % base.root_templates
    conf_path = base.write_template(
        c,
        file_path="%s/ipsec.conf" % template_folder,
        destination_path="/tmp/",
        template_context={
            'server_ip': c.host
        },
        sudo=True
    )
    secrets_path = base.write_template(
        c,
        file_path="%s/ipsec.secrets" % template_folder,
        destination_path="/tmp/",
        template_context={
            'username': username,
            'password': password
        },
        sudo=True
    )
    base.write_template(
        c,
        file_path="%s/sysctl.conf" % template_folder,
        destination_path="/etc/sysctl.conf",
        sudo=True
    )
    c.run('sudo sysctl -p')
    install_script = base.write_template(
        c,
        file_path="%s/configure_script.sh" % template_folder,
        destination_path="/tmp/",
        template_context={
            'vpn_name': vpn_name,
            'server_ip': c.host,
            'ssh_port': ssh_port,
            'conf_path': conf_path,
            'secrets_path': secrets_path
        }
    )
    c.run('/bin/bash %s' % install_script)
    c.get('/etc/ipsec.d/cacerts/ca-cert.pem')
    c.sudo('reboot')
