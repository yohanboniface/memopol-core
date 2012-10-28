from categories.models import Category

from ajax_select import LookupChannel


class MepAchievements(LookupChannel):
    model = Category
    search_field = "name"
    min_length = 3
    plugin_options = {
        "minLength": min_length,
    }

    def format_item_custom(self, obj):
        """
        Additional, custom data for an item, returned in the json.
        Can override any of the default fields (pk, label, value, repr)
        if necessary, although it's not recommended.
        """
        return {
            "pk": obj.slug  # We index slug to make it usable in parsed
                            # query string mode
        }
