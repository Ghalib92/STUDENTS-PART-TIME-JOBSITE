# chat/context_processors.py
from .models import Thread, Message

def unread_message_count(request):
    if request.user.is_authenticated:
        threads = Thread.objects.filter(
            employer=request.user
        ) | Thread.objects.filter(
            jobseeker=request.user
        )

        count_dict = {}
        for thread in threads:
            unread = thread.messages.filter(is_read=False).exclude(sender=request.user).count()
            other_user = thread.jobseeker if thread.employer == request.user else thread.employer
            if unread > 0:
                count_dict[other_user.id] = unread

        return {'unread_messages': count_dict}
    return {}
