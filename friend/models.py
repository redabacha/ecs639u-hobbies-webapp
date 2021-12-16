from django.conf import settings
from django.db import models

class FriendList(models.Model):

	user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
	friends= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="friends") 

	def addFriend(self, profile):
		if profile not in self.friends.all():
			self.allFriends.add(profile)

	def deleteFriend(self, profile):
		if profile in self.friends.all():
			self.friends.remove(profile)

	def __str__(self):
		return self.user.username


class FriendRequest(models.Model):

	senderOfRequest= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="senderOfRequest")
	receiverOfRequest= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recieverOfRequest")


	def acceptFriendRequest(self):
		receiverFriendList = FriendList.objects.get(user=self.receiverOfRequest)
		if receiverFriendList:
			receiverFriendList.addFriend(self.senderOfRequest)

			senderFriendList = FriendList.objects.get(user=self.senderOfRequest)
			if senderFriendList:
				senderFriendList.addFriend(self.receiverOfRequest)


	def deleteFriendRequest(self):
		receiverFriendList = FriendList.objects.get(user=self.receiverOfRequest)
		if receiverFriendList:
			receiverFriendList.deleteFriend(self.senderOfRequest)

			senderFriendList = FriendList.objects.get(user=self.senderOfRequest)
			if senderFriendList:
				senderFriendList.deleteFriend(self.receiverOfRequest)

	def __str__(self):
		return self.senderOfRequest.username