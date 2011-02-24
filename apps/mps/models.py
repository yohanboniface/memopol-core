from couchdbkit.ext.django.schema import Document, StringProperty

class MP(Document):
    id = StringProperty()
    extid = StringProperty()
    name = StringProperty()

