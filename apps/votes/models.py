from couchdbkit.ext.django.schema import Document, StringProperty, DateTimeProperty

class Vote(Document):
    last_datetime = DateTimeProperty
    label = StringProperty()
    wiki = StringProperty()

