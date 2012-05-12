Introduction
============

The Political Memory is a tool build by [la Quadrature du Net](http://lqdn.fr).
It follow several objectives: being a campaign tool, being able to display how
well the elected representatives have followed the voting recommendations of la
Quadrature du Net, increase the political cost of the decisions of elected
representatives, gather official positions taken by elected representatives
and, the most important one, inform citizens.

This is the second version of the tool.

Links
=====

* [code](http://gitorious.org/memopol2-0) (and there is also a mirror on [github](https://github.com/Psycojoker/memopol2))
* [official la Quadrature du Net's instance](https://memopol.lqdn.fr)
* [Bug tracker](https://projets.lqdn.fr/projects/mempol)
* [dev blog](http://memopol.org)
* [mailing list](http://laquadrature.net/cgi-bin/mailman/listinfo/mempol2)

We also have an irc channel: irc.freenode.net#lqdn-memopol (english speaking but if you only know french we can deal with that) where you will be very welcome

How to contribute
=================

Like in any free software project:

* clone it
* install it
* code
* optional: talk to us about it on irc or on the mailing list
* send a pull request either on [gitorious](http://gitorious.org/memopol2-0) or [github](https://github.com/Psycojoker/memopol2)
* hit us with a stick if we don't react (shouldn't happen)
* we merge your code, everyone is happy
* party hard
* start again

You can see the list of our awesome contributors in CREDITS.txt (if someone is missing just tell me).

Installation
============

Debian and debian-based
-----------------------

Install the base python virtualenv tools (on Ubuntu you have to enable universe):

    sudo apt-get install python-setuptools python-dev libxml2-dev libxslt1-dev libfreetype6-dev libpng12-dev python-pip libatlas-base-dev g++ mercurial git libtidy-dev
    sudo pip install virtualenv

Archlinux
---------

Install the following to have the tools on Archlinux (please note that you may have to adapt the following install procedure):

    pacman -S python2 libxml2 libxslt freetype2 python-lxml python2-pip python2-virtualenv libpng mercurial git

Fedora
------

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
*LOTS* of time, around 15min.

    cd memopol2
    ./INIT

Do *not* try to run migrate by hand or you will have a bug due to fixtures
loading and will end up with no eurodeputies fixtures.

Run the server
--------------

    cd memopol2
    python manage.py runserver

Your application is available on http://localhost:8000/

Small lexicon
=============

We try not to use it too much but you'll eventually end up on it so here is a
reference.

* "mep" == member of the European Parliament
* "mp" == member of the Parliament, here it's deputies of the French national assemble

Licence
=======

The Political is licenced under aGPLv3+. The original idea is from [gibus](http://gibus.sedrati-dinet.net/).
