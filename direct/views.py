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
  print(to_user)
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
  context = {
      'messages': messages,
      'directs': directs,
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
  