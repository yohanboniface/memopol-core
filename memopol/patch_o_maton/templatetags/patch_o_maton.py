from django import template
import diff_match_patch

register = template.Library()

@register.filter()
def asdiff(obj):
   de=diff_match_patch.diff_match_patch()
   diffs=de.diff_main(' '.join(obj.old.split('\n')),' '.join(obj.new.split('\n')))
   de.diff_cleanupSemantic(diffs)
   return de.diff_prettyHtml(diffs)

@register.filter()
def totalscore(obj):
   return sum([x.score for x in obj.score_set.all()])
