from django.contrib import admin

from hyperion.models import *

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Server)
admin.site.register(Friend)
admin.site.register(FriendRequest)
