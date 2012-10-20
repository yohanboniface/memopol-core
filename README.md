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

Running tests
-------------

Projects tests are centralized in the `tests` dir.

To run tests, you just need to run `nosetests` in the project root directory.

The nose configuration is in the `setup.cfg` file.


Installation
============

Debian and debian-based
-----------------------

Install the base python virtualenv tools (on Ubuntu you have to enable universe):

    sudo apt-get install python-setuptools python-dev libxml2-dev libxslt1-dev libfreetype6-dev libpng12-dev python-pip libatlas-base-dev g++ mercurial git libtidy-dev imagemagick
    sudo pip install virtualenv

Archlinux
---------

Install the following to have the tools on Archlinux (please note that you may have to adapt the following install procedure):

    pacman -S python2 libxml2 libxslt freetype2 python-lxml python2-pip python2-virtualenv libpng mercurial git imagemagick tidyhtml

Fedora
------

Install the following to have the tools on Fedora (please note that you may have to adapt the following install procedure):

    yum install python-setuptools python-devel libxml2-devel libxslt-devel freetype freetype-devel libpng libpng-devel python-lxml python-pip atlas-devel g++ mercurial git imagemagick

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

Warning: this might take a *LOTS* of time, around 15min.

    python manage.py init

Do *not* try to run migrate by hand or you will have a bug due to fixtures
loading and will end up with no eurodeputies fixtures.

Run the server
--------------

    python manage.py runserver

Your application is available on http://localhost:8000/

And you're done, but you might want to take a look at the next section
depanding on what you want to dev.

Updating memopol's data
=======================

Update European Parliament related data
---------------------------------------

Just run:

    python manage.py update_meps

This might take some time. Be sure to do that after having run "init".

Adding a voting recommendation
------------------------------

First, you have to get all the votes data by running this command:

    python manage.py import_ep_votes_data

If you want to update the available importables votes, just re-run this
command.

Then you need chose a vote on which you want to create a recommendation. For
this: got to `/votes/import/` on your instance (for example:
http://mempol2.serverside.fr/votes/import/). There, you'll see the list of the
importable votes (with not very user friendly name, those are the one given by
the European Parliament). Chose a vote, click on it, grab it's "ID" as
specified on his page, then run:

    python manage.py create_voting_recommandation <vote id> <{for,against}> <weight of the recommendation> <weight of the proposal, 1 by default>

Where: the `vote id` is the idea you have chosen, `for` or `against` is your
voting recommendation, `weight of the recommendations` is the weight you want
to give to the recommendation (for exemple: the weight of the final vote is way
more important than the one of a small amendment) and weight of the proposal is
the weight of the total vote (for example: the vote on ACTA is way more
important than the Lambrinidis rapport for la Quadrature du Net).

Example:

    python manage.py create_voting_recommendation 8838 for 3 3

**WARNING**: due to the nature of the data, this last command has
non-negligible chances of failing.

Personalization
===============

Change the organization name
----------------------------

You can change the organization name displayed on the header in
`memopol2/settings.py` by changing the `ORGANIZATION_NAME` variable.

Remove la Quadrature du Net data from Memopol
---------------------------------------------

If you want to remove this data to use memopol for your own cause (yay \o/) a
command is ready for you:

    python manage.py remove_lqdn_data

This will remove everything related to the votes that we are tracking and the
opinions. More customisability will appears in the future and better doc on how
to use the cli tools.

Small lexicon
=============

We try not to use it too much but you'll eventually end up on it so here is a
reference.

* "mep" == member of the European Parliament
* "mp" == member of the Parliament, here it's deputies of the French national assemble

Licence
=======

The Political is licenced under aGPLv3+. The original idea is from [gibus](http://gibus.sedrati-dinet.net/).
