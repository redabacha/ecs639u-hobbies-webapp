from django.contrib import admin
from friend.models import FriendList, FriendRequest

class FriendListAdmin(admin.ModelAdmin):
    listFilter = ['user']
admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    listFilter = ['senderOfRequest', 'receiverOfRequest']
admin.site.register(FriendRequest, FriendRequestAdmin)
