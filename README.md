Installation
============

Install the base dependencies on debian-based distributions
-----------------------------------------------------------

Install the base python virtualenv tools (on Ubuntu you have to enable universe):

    sudo apt-get install python-setuptools python-dev libxml2-dev libxslt1-dev libfreetype6-dev libpng12-dev python-pip libatlas-base-dev g++ mercurial git
    sudo pip install virtualenv

Install the base dependencies on ArchLinux
------------------------------------------

Install the following to have the tools on Archlinux (please note that you may have to adapt the following install procedure):

    pacman -S python2 libxml2 libxslt freetype2 python-lxml python2-pip python2-virtualenv libpng mercurial git

Install the base dependencies on Fedora
---------------------------------------

Install the following to have the tools on Fedora (please note that you may have to adapt the following install procedure):

    yum install python-setuptools python-devel libxml2-devel libxslt-devel freetype freetype-devel libpng libpng-devel python-lxml python-pip atlas-devel g++ mercurial git

    pip-python install virtualenv


Installing python dependencies
------------------------------

We are using a virtualenv (there is everything needed to use buildout also if you want to).

Create one:

    virtualenv --no-site-packages --distribute ve

Active it:

    source ve/bin/activate

(If you want to leave it just type "deactivate")

Install memopol2's dependencies (yes you need to build numpy alone first):

    pip install numpy==1.5.1
    pip install -r requirements.txt


Run the "migration" scripts
---------------------------

Run syncdb then migrate, this will import the fixtures. Warning: this take a
*LOTS* of time, arround 15min.

    cd memopol2
    ./INIT

Do *not* try to run migrate by hand or you will have a bug due to fixtures
loading and will end up with no meps fixtures.

Run the server
--------------

    cd memopol2
    python manage.py runserver

Your application is available on http://localhost:8000/
