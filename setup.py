import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

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
    install_requires = [],
    entry_points = """
    [console_scripts]
    gen_templates = memopol2.scripts:gen_templates
    """
)
