from datetime import timedelta

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from .models import Diary, Entry, Feeling
from .forms import AddEntryForm

@login_required
def index(request):
    return render(request, 'howifeel/index.html')

@login_required
def view_diary(request):
    return HttpResponse("View last few entries")

@login_required
def view_entry(request, entry_id):
    entry = Entry.objects.get(user=request.user, pk=entry_id)
    return render(request, 'howifeel/view_entry.html',
                  { 'entry': entry })

@login_required
def add_entry(request):
    user = request.user
    form = AddEntryForm(user=user)
    if request.method == 'POST':
        if request.POST['diary'] == '':
            diary = Diary.objects.get(user=user, name="Untitled")
        else:
            diary = Diary.objects.get(user=user, pk=int(request.POST['diary']))

        date = request.POST['date']
        title = request.POST['title']
        text = request.POST['text'].replace("\n", "<br>")

        print(text)

        energy = int(request.POST['energy'])
        mood = int(request.POST['mood'])

        entry = Entry(user=user, diary=diary, date=date, title=title, text=text,
                      energy=energy, mood=mood)
        entry.save()

        raw_feelings = request.POST['feelings']
                
        feeling_words = [f.strip().lower() for f in raw_feelings.split(",")]

        for feeling_word in feeling_words:
            try:
                feeling = Feeling.objects.get(user=user, name=feeling_word)
            except:
                feeling = Feeling(user=user, name=feeling_word)
                feeling.save()  # in case feeling does not exist
            entry.feelings.add(feeling)

        return HttpResponseRedirect('../entry_added/')

    return render(request, 'howifeel/add_entry.html', { 'form': form })

@login_required
def search(request):
    if request.method == 'POST':
        search_parameter = request.POST['search_parameter']
        entries = (Entry.objects.filter(user=request.user)
                   .filter(Q(text__icontains=search_parameter)
                           | Q(title__icontains=search_parameter))
                   .order_by('-date'))
        return render(request, 'howifeel/list_entries.html',
                      { 'entry_category': "search results",
                        'entries': entries })
    return render(request, 'howifeel/search_form.html')
    
@login_required
def entry_added(request):
    return render(request, 'howifeel/entry_added.html')

@login_required
def list_entries(request):
    all_entries = Entry.objects.filter(user=request.user).prefetch_related('feelings').order_by('-date')
    return render(request, 'howifeel/list_entries.html',
                  { 'entry_category': "All", 'entries': all_entries })

@login_required
def list_feelings(request):
    all_feelings = Feeling.objects.filter(user=request.user).order_by('name')
    return render(request, 'howifeel/list_feelings.html',
                  { 'feelings': all_feelings })

@login_required
def entries_by_feeling(request, feeling_id):
    entries = Entry.objects.filter(user=request.user, feelings__pk=feeling_id)
    feeling_obj = Feeling.objects.get(user=request.user, pk=feeling_id)
    return render(request, 'howifeel/list_entries.html',
                  { 'entry_category': 'feeling ' + str(feeling_obj),
                    'entries': entries })

@login_required
def graph(request):
    today = timezone.now()
    last_week = today - timedelta(days=7)
    entries = (Entry.objects.filter(user=request.user)
               # date__gte=today-timedelta(days=7)).
               .order_by('-date'))
    return render(request, 'howifeel/graph.html',
                  { 'entries': entries,
                    'today': today,
                    'last_week': last_week })
