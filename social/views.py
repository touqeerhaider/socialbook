from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect

from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView
from rest_framework import viewsets

from social.myserializer import MyProfileSerializer, MyPostSerializer, PostLikeSerializer, PostCommentSerializer, \
    FollowUserSerializer
from social.models import MyProfile, MyPost, PostLike, PostComment, FollowUser
from django.db.models import Q


@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "social/home.html"

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        followedlist = FollowUser.objects.filter(followed_by=self.request.user.myprofile)
        followedlistprofile = []
        for e in followedlist:
            followedlistprofile.append(e.profile)
        si = self.request.GET.get("si")
        if si is None:
            si = ""
        posts = MyPost.objects.filter(Q(uploaded_by__in=followedlistprofile)).filter(Q(subject__icontains=si) | Q
        (msg__icontains=si)).order_by("-id")
        for p1 in posts:
            p1.liked = False
            ob = PostLike.objects.filter(post=p1, liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True
            ob = PostLike.objects.filter(post=p1)
            p1.likecount = ob.count()
        context["mypost_list"] = posts
        return context


class AboutView(TemplateView):
    template_name = "social/about.html"


class ContactView(TemplateView):
    template_name = "social/contact.html"


def follow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by=req.user.myprofile)
    return HttpResponseRedirect(redirect_to='/social/myprofile/')


def unfollow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by=req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to='/social/myprofile/')


def like(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by=req.user.myprofile)
    return HttpResponseRedirect(redirect_to='/social/home/')


def unlike(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by=req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to='/social/home/')


@method_decorator(login_required, name="dispatch")
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "age", "address", "status", "gender", "phone_no", "descriptions", "pic"]


@method_decorator(login_required, name="dispatch")
class MyPostCreateView(CreateView):
    model = MyPost
    fields = ["subject", "msg", "pic"]

    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")
class MyPostListView(ListView):
    model = MyPost

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si is None:
            si = ""
        return MyPost.objects.filter(Q(uploaded_by=self.request.user.myprofile)).filter(Q(subject__icontains=si) | Q
        (msg__icontains=si)).order_by("-id")


@method_decorator(login_required, name="dispatch")
class MyPostDetailView(DetailView):
    model = MyPost


@method_decorator(login_required, name="dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost


class MyProfileListView(ListView):
    model = MyProfile

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si is None:
            si = ""
        proflist = MyProfile.objects.filter(~Q(user=self.request.user)).filter(Q(name__icontains=si) |
        Q(address__icontains=si) | Q(age__icontains=si) | Q(gender__icontains=si)).order_by("-id")

        for p1 in proflist:
            p1.followed = False
            ob = FollowUser.objects.filter(profile=p1, followed_by=self.request.user.myprofile)
            if ob:
                p1.followed = True
        return proflist


@method_decorator(login_required, name="dispatch")
class MyProfileDetailView(DetailView):
    model = MyProfile


class MyProfileViewSet(viewsets.ModelViewSet):
    queryset = MyProfile.objects.all().order_by('-id')
    serializer_class = MyProfileSerializer

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si is None:
            si = ""
        return MyProfile.objects.filter(Q(name__icontains=si) |
        Q(address__icontains=si) | Q(age__icontains=si) | Q(gender__icontains=si)).order_by("-id")


class MyPostViewSet(viewsets.ModelViewSet):
    queryset = MyPost.objects.all().order_by('-id')
    serializer_class = MyPostSerializer

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si is None:
            si = ""
        return MyPost.objects.filter(Q(subject__icontains=si) | Q
        (msg__icontains=si)).order_by("-id")


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all().order_by('-id')
    serializer_class = PostLikeSerializer


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all().order_by('-id')
    serializer_class = PostCommentSerializer


class FollowUserViewSet(viewsets.ModelViewSet):
    queryset = FollowUser.objects.all().order_by('-id')
    serializer_class = FollowUserSerializer


