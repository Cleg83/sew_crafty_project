from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import Events
from .forms import EventForm

# Create your views here.
def upcoming_events(request):
    """ View to show upcoming events """

    today = timezone.now().date()  
    events = Events.objects.filter(start_date__gte=today).order_by('start_date')
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
        if not query:
            messages.error(request, 'Please enter some search criteria!')
            return redirect(reverse('events'))

        queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        events = events.filter(queries)

    context = {
        'events': events,
        'search_criteria': query,
    }

    return render(request, 'events/events.html', context)


def manage_events(request):
    """Similar to event list view but with editing options"""
    if not request.user.is_superuser:
        messages.error(request, "You do not have the necessary permissions to access this page.")
        return redirect('home')

    events = Events.objects.all().order_by('start_date')

    template = 'events/manage_events.html'

    context = {
        'events': events,
    }

    return render(request, template, context)


def add_event(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have the necessary permissions to perform this action.")
        return redirect('home')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('manage_events')  
    else:
        form = EventForm()

    context = {
        'form': form,
        'action': 'Add'
    }
    return render(request, 'events/add_event.html', context)


def edit_event(request, event_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have the necessary permissions to perform this action.")
        return redirect('home')
    
    event = get_object_or_404(Events, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('manage_events')  
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'action': 'Update',
        'event': event
    }
    return render(request, 'events/edit_event.html', context)


def delete_event(request, event_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have the necessary permissions to perform this action.")
        return redirect('home')
    
    event = get_object_or_404(Events, id=event_id)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('manage_events')  
