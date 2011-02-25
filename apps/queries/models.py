from couchdbkit.ext.django.schema import Document, StringProperty

# Create your models here.
class MEP(Document):
    id = StringProperty()
