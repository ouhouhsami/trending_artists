import autocomplete_light
from .models import Artist

# This will generate a PersonAutocomplete class
autocomplete_light.register(Artist,
    # Just like in ModelAdmin.search_fields
    search_fields=['name', ],
    # This will actually html attribute data-placeholder which will set
    # javascript attribute widget.autocomplete.placeholder.
    autocomplete_js_attributes={'placeholder': 'Artist name ?',},
)
