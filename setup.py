import distribute_setup
distribute_setup.use_setuptools()

import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

    
setup(
    name='Memopol',
    version = '1.99.1',
    author = 'The memopol project',
    author_email = 'deubeulyou@gmail.com',
    description = 'Memoire Politique',
    long_description = read_file('README.txt'),
    license = 'LICENSE.txt',
    url = 'http://projets.lqdn.fr/projects/mempol',
    packages = find_packages(),
    include_package_data = True,
    scripts = ['bin/jenkins-setup-and-test.sh'],
    install_requires = read_file('requirements.txt'),
    extras_require = {
        'test': read_file('requirements-test.txt')
    }
)
