Memopol2 is a django+couchdb rewrite of the incredibly useful Memoire
Politique tool.

Installation
============
See /docs/SETUP.txt

Hacking
=======
See /docs/HACKING.txt

Overall goals
=============

Memopol is a project created by La Quadrature du Net to achieve the
following goals:
- Providing a framework to political activists in order to optimize,
show and promote their actions.
- Providing world citizens an accurate view of their political
representatives actions in parliaments and assemblies.
- Raising the political cost for representatives of taking bad decisions
by attributing good and bad points (needs strong, friendly visual layer).

Memopol V1
==========

- A set of scripts to dump the official list of EU parliaments
members, French deputies from official sites and import it in a database
- A webapp to display european parliamentarians, their groups, their
commissions in various ways, and also their opinions (transcripts of
public talks)
- A ranking system: Confronting the nominative votes of
parliamentarians and the Quadrature's "reading grid" provides a score
for each of them.
- All this is wrapped in mediawiki.
- http://www.laquadrature.net/wiki/Memoire_politique

Limitations
-----------

- The database is hard to maintain: changes on official sources must
be noticed by someone, otherwise the DB is not up to date; the
modifications themselves are done a very few set of people which can
induce another lag
- Some tools are missing or need polishing. For instance, we have a
simple way to know which parliamentarian we should contact for an
upcoming vote, but no way to really distribute the effort efficiently;
also, the view (big table with percentages) of the vote results is not
very readable.
- The system is composed of a lot of subsystems which are not really
centralized, making the ball hard to catch for new developers.

Memopol V2
==========

The main goals are to fix what I described in the limitations. A new
python/django/couchdb system has already been developed, but some
features are still missing to reach the V1, so we have to catchup. I
attached a very nasty text file which explains where we are and
propose some "around applications". Also, I want to state that another
goal is clearly to switch from an internal tool to a bundled
application, allowing it to be reusable, extensible and all the
goodness of the community based efforts.

