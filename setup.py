#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(
name = "memopol",
version = "0.1",
packages = find_packages('.'),
package_dir = {'':'.'},

include_package_data = True,
zip_safe = False,

# author metadata
author = 'The memopol project',
author_email = 'deubeulyou@gmail.com',
description = 'Memoire Politique',
url = 'http://projets.lqdn.fr/projects/mempol',
)
