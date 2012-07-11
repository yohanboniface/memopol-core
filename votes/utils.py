import os
from django.conf import settings

def clean_all_trends():
    for directory in os.walk(settings.MEDIA_DIRECTORY + "img/trends/"):
        for file in directory[-1]:
            file_path = "%s/%s" % (directory[0], file)
            if os.path.isfile(file_path):
                os.remove(file_path)
