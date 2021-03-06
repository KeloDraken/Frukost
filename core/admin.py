from django.contrib import admin

from core.models import (
    Feedback,
    News,
    Privacy,
    Rules,
    Subscribers,
    Terms,
)

admin.site.register(News)
admin.site.register(Feedback)

admin.site.register(Subscribers)

# Legal
admin.site.register(Rules)
admin.site.register(Terms)
admin.site.register(Privacy)
