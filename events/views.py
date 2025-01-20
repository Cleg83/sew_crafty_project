from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Events
from .forms import EventForm

# Create your views here.
def upcoming_events(request):
    """ View to show upcoming events """

    events = Events.objects.all().order_by('start_date')

    context = {
        'events': events,
    }

    return render(request, 'events/events.html', context)


def events_list_view(request):
    """ List view to show upcoming events """

    events = Events.objects.all().order_by('start_date')
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
        if not query:
            messages.error(request, 'Please enter some search criteria!')
            return redirect(reverse('events/list'))

        queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        events = events.filter(queries)

    context = {
        'events': events,
        'search_criteria': query,
    }

    return render(request, 'events/events_list_view.html', context)


@login_required
def manage_events(request):
    """Similar to event list view but with editing options"""

    events = Events.objects.all().order_by('start_date')

    template = 'events/manage_events.html'

    context = {
        'events': events,
    }

    return render(request, template, context)


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('events_list_view')  
    else:
        form = EventForm()

    context = {
        'form': form,
        'action': 'Add'
    }
    return render(request, 'events/edit_event.html', context)

# Update Event View
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events_list_view')  
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'action': 'Update',
        'event': event
    }
    return render(request, 'events/edit_event.html', context)


# Delete Event View
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('events_list_view')  
