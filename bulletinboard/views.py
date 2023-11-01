from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def bulletinboard(request):
    posts = Post.objects.all()
    return render(request, 'BulletinBoard/bulletinboard.html', {'posts': posts})

def post(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'BulletinBoard/posts.html', {'posts': posts})