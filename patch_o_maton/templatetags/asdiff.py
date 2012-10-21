from django import template
import diff_match_patch

register = template.Library()

@register.filter()
def asdiff(obj):
   de=diff_match_patch.diff_match_patch()
   diffs=de.diff_main(' '.join(obj.old.split('\n')),' '.join(obj.new.split('\n')))
   de.diff_cleanupSemantic(diffs)
   return de.diff_prettyHtml(diffs)
