from fabs.mac import patches
from fabs.mac import system
from invoke import Collection, task
from pathlib import Path


home = str(Path.home())


@task
def safari_cache_clean(c, action):
    cmd = "rm -rf %s/Library/Caches/com.apple.Safari/Cache.db" % home
    system.cron(c, action, '0', '*', '*', '*', '*', cmd, 'Caches.*Safari')


namespace = Collection(patches, system, safari_cache_clean)
