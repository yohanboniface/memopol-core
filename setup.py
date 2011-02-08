import distribute_setup
distribute_setup.use_setuptools()

import os
from setuptools import setup, find_packages

def find_files(dirname):
    files = []
    for entryname in os.listdir(dirname):
        pathname = "%s/%s" % (dirname, entryname)
        if os.path.isfile(pathname):
            files.append(pathname)
        elif os.path.isdir(pathname):
            files += find_files(pathname)        
    return files
    
setup(
    name='Memopol',
    version = '1.99.1',
    author = 'The memopol project',
    author_email = 'deubeulyou@gmail.com',
    description = 'Memoire Politique',
    long_description = open('README.txt').read(),
    license = 'LICENSE.txt',
    url = 'http://projets.lqdn.fr/projects/mempol',
    packages = find_packages(),
    include_package_data = True,
    scripts = find_files('bin'),
    install_requires = open('requirements.txt').read(),
    extras_require = {
        'test': open('requirements-test.txt').read()
    }
)
