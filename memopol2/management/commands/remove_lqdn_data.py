from django.db import transaction, connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'remove data specific to lqdn to be used by another organization'

    def handle(self, *args, **options):
        print "Warning, this command is VERY dangerous"
        print "This will remove every data related to lqdn: votes and opinions"
        if raw_input("If you are sure that you know what you are doing, write 'yes': ") != "yes":
            print "Didn't got yes, abort"
            return

        # I don't like using raw sql here but django orm sucks for this task
        # and will nomnom too much ram for nothing

        print "Removing votes..."
        connection.cursor().execute("DELETE FROM votes_vote")
        print "Removing recommendations..."
        connection.cursor().execute("DELETE FROM votes_recommendation")
        print "Removing scores..."
        connection.cursor().execute("DELETE FROM votes_score")
        print "Removing proposals..."
        connection.cursor().execute("DELETE FROM votes_proposal")
        print "Removing opinions..."
        connection.cursor().execute("DELETE FROM reps_opinion")
        transaction.commit_unless_managed()
