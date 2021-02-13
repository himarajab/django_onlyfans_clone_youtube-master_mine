from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from tier.models import Tier,Subscription
from post.models import Post,PostFileContent,Stream,Likes
from post.forms import NewPostForm
from django.shortcuts import redirect, render,get_object_or_404

@login_required
def index(request):
  user =request.user
  # all posts from user u subscribe to them
  stream_items = Stream.objects.filter(user=user).order_by('date')
  
  #Pagination
  paginator = Paginator(stream_items, 9)
  page_number = request.GET.get('page')
  
  stream_data = paginator.get_page(page_number)
  # stream_data = [1]
  print(stream_data)
  # return True
  context = {
      'stream_data': stream_data,
  }

  return render(request, 'index.html', context)


@login_required
def post_details(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    #Check if the user liked the post
    if Likes.objects.filter(post=post, user=user).exists():
        liked = True
    else:
        liked = False
    

    # To validate that the user can see the post
    if user != post.user:
        subscriber = Subscription.objects.get(subscriber=request.user, subscribed=post.user)
        if (subscriber.tier.number >= post.tier.number):
            visible = True
        else:
            visible = False
    # else:
    #     visible = True
    
    context = {
        'post': post,
        'visible': visible,
        'liked': liked,
        # 'comments': comments,
        # 'form': form,
    }

    return render(request, 'post_detail.html', context)


def new_post(request):
  user = request.user
  files_objs = []

  if request.method == "POST":
      form = NewPostForm(request.POST, request.FILES)

      if form.is_valid():
          files = request.FILES.getlist('content')
          title = form.cleaned_data.get('title')
          caption = form.cleaned_data.get('caption')
          tier = form.cleaned_data.get('tier')
          tiers = get_object_or_404(Tier, id=tier.id)

          for file in files:
              file_instance = PostFileContent(file=file, user=user, tier=tiers)
              file_instance.save()
              files_objs.append(file_instance)
          
          p, created = Post.objects.get_or_create(title=title, caption=caption, user=user, tier=tiers)
          p.content.set(files_objs)
          p.save()
          return redirect('index')
  else:
      form = NewPostForm()
      form.fields['tier'].queryset = Tier.objects.filter(user=user)
  
  context = {
      'form': form,
  }

  return render(request, 'new_post.html', context)


@login_required
def like(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    current_likes = post.likes_count

    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
    
    post.likes_count = current_likes
    post.save()

    return HttpResponseRedirect(reverse('post-detail', args=[post_id])) 