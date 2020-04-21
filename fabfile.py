from fabs.ubuntu import base
from fabs.ubuntu import system
from fabs.ubuntu import packages
from invoke import Collection
namespace = Collection(base, system, packages)
