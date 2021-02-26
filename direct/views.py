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