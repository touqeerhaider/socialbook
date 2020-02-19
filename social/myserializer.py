from django.contrib.auth.models import User
from rest_framework import serializers
from social.models import MyProfile, MyPost, PostLike, PostComment, FollowUser


class MyProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyProfile
        fields = ["name", "age", "address", "status", "gender", "phone_no", "descriptions", "pic"]


class MyPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyPost
        fields = "__all__"


class PostLikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"


class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"


class FollowUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FollowUser
        fields = "__all__"