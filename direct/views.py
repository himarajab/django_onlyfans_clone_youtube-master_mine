from django.contrib.humanize.templatetags import humanize
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from direct.models import Message
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tier.models import Subscription, Tier
from django.shortcuts import redirect, render,get_object_or_404

@login_required
def people_we_can_message(request):
  #  all Subscription for this user and he can also send messages to them
  people = Subscription.objects.filter(Q(subscriber=request.user) & Q(tier__can_message=True))
  context = {
    'people':people,

  }

  return render(request,'direct/can_message_list.html',context)



@login_required
def new_conversation(request,username):
  from_user = request.user
  to_user = get_object_or_404(User,username=username)
  body = 'started a new conversation'

  # can't send message to your self
  if from_user != to_user:
    # person who will start the conversation create message for the person will send the message 
    # not for tow objects like the send_message method
    Message.objects.create(user=from_user,sender=from_user,body=body,recipient=to_user)
  return redirect('inbox')

@login_required
def inbox(request):
  messages = Message.get_messages(user=request.user)
  
  
  #Pagination
  paginator_messages = Paginator(messages, 5)
  page_number_messages = request.GET.get('messagespage')
  
  messages_data = paginator_messages.get_page(page_number_messages)
  # stream_data = [1]
  # return True
  
  
  context = {
      'messages': messages_data,
  }

  return render(request,'direct/inbox.html',context)


@login_required
def directs(request,username):
  user = request.user
  # load all the conversation
  messages = Message.get_messages(user=request.user)
  active_direct = username
  # messages
  directs = Message.objects.filter(user=user,recipient__username=username).order_by('-date')

  for message in messages:
    if message['user'].username == username:
      # delete all unread messages
      message['unread'] =0
  #Pagination for directs
  paginator_directs = Paginator(directs, 5)
  page_number_directs = request.GET.get('directspage')
  
  directs_data = paginator_directs.get_page(page_number_directs)
  # stream_data = [1]
  # return True
  context = {
      'directs': directs_data,
      'messages': messages,
      'active_direct': active_direct,
  }

  return render(request,'direct/direct.html',context)


@login_required
def send_direct(request):
  from_user = request.user
  to_user_username = request.POST.get('to_user')
  body = request.POST.get('body')


  if request.method == 'POST':
    to_user = get_object_or_404(User,username=to_user_username)
    Message.send_message(from_user=from_user,to_user=to_user,body=body)
    return HttpResponseRedirect(reverse('directs', args=[to_user_username]))
  else:
    HttpResponseBadRequest()
  

def load_more(request):
  user = request.user

  if request.is_ajax():
    username = request.POST.get('username')
    page_number_directs = request.POST.get('directspage')
    # load the messages and get the values before send it to json
    directs = Message.objects.filter(user=user,recipient__username=username).order_by('-date').values(
      'sender__profile__picture',
      'sender__first_name',
      'sender__last_name',
      'body',
      'date'
    )

    #Pagination for directs
    paginator_directs = Paginator(directs, 5)
    # if we on the same page number
    if paginator_directs.num_pages >= int(page_number_directs):
      # get the page data if it's a page in range (vaild number)
      directs_data = paginator_directs.get_page(page_number_directs)


      # create list of data 
      directs_list = list(directs_data)

      # replace the default date with humenize valid  date for json 
      for message in range(len(directs_list)):
        directs_list[message]['date'] = naturaltime(directs_list[message]['date'])
      
      return JsonResponse(directs_list,safe=False)
    else:
      return JsonResponse({'empty':True},safe=False)


@login_required
def user_search(request):
  query = request.GET.get('q')
  users_paginator = None

  if query:
    users = Subscription.objects.filter(Q(subscribed__username__icontains=query) & Q(tier__can_message=True))
    
    #Pagination 
    paginator = Paginator(users, 6)
    page_number = request.GET.get('directspage')
    
    users_paginator = paginator.get_page(page_number)

  context = {
      'users': users_paginator,
      
  }

  return render(request,'direct/search_user.html',context)