# -*- coding:Utf-8 -*-

import os
import sys
import ijson
from os.path import join
from json import dumps
from dateutil.parser import parse

from django.db import transaction, connection, reset_queries
from django.core.management.base import BaseCommand
from django.conf import settings

from memopol.votes.models import RecommendationData


class Command(BaseCommand):
    help = 'Import vote data of the European Parliament, this is needed to be able to create voting recommendations'

    def handle(self, *args, **options):
        print "Clean old downloaded files"
        os.system("rm %s %s" % (join(settings.MEMOPOL_TMP_DIR, "ep_votes.json"), join(settings.MEMOPOL_TMP_DIR, "ep_votes.json.xz")))
        print "Download vote data from parltrack"
        os.system("wget -O %s http://parltrack.euwiki.org/dumps/ep_votes.json.xz" % join(settings.MEMOPOL_TMP_DIR, "ep_votes.json.xz"))
        print "unxz it"
        os.system("unxz %s" % join(settings.MEMOPOL_TMP_DIR, "ep_votes.json.xz"))
        print "cleaning old votes data..."
        connection.cursor().execute("DELETE FROM votes_recommendationdata")
        transaction.commit_unless_managed()
        print RecommendationData.objects.count()
        print "read file"
        a = 1
        with transaction.commit_on_success():
        # I need to parse the json file by hand, otherwise this eat way to much memory
            for vote in ijson.items(open(join(settings.MEMOPOL_TMP_DIR, "ep_votes.json")), 'item'):
                    RecommendationData.objects.create(proposal_name=vote.get("report", vote["title"]),
                                                     title=vote["title"],
                                                     data=dumps(vote, indent=4),
                                                     date=parse(vote["ts"])),
                    reset_queries()
                    sys.stdout.write("%s\r" % a)
                    sys.stdout.flush()
                    a += 1
            sys.stdout.write("\n")

# vim:set shiftwidth=4 tabstop=4 expandtab:
