from fabric import task


@task
def b2_delete(c, bucket, prefix, file_regex=None, shell_env=None):
    shell_env = shell_env or {}
    if(file_regex):
        return c.run("b2 ls --recursive --long --versions %s %s | grep %s | while read c1 x x x x c6; do b2 delete-file-version $c6 $c1; done" % (
            bucket, prefix, file_regex
        ), env=shell_env)
    c.run("b2 ls --recursive --long --versions %s %s | while read c1 x x x x c6; do b2 delete-file-version $c6 $c1; done" % (bucket, prefix), env=shell_env)
