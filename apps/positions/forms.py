from django import forms
from django.contrib.comments.forms import CommentForm
from django.utils.translation import ugettext as _
from django.conf import settings

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

class PositionForm(CommentForm):
    name          = forms.CharField(label=_("Name"), max_length=50, required=False)
    email         = forms.EmailField(label=_("Email address"), required=False)
    url           = forms.URLField(label=_("Source"), required=True)
    comment       = forms.CharField(label=_('Position'), widget=forms.Textarea,
                                    max_length=COMMENT_MAX_LENGTH)
