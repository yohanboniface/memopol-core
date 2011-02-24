from couchdbkit.ext.django.schema import Document, StringProperty

class Vote(Document):
    label = StringProperty()
    wiki = StringProperty()

