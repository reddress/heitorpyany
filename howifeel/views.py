from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Diary, Entry, Feeling
from .forms import AddEntryForm

@login_required
def index(request):
    return render(request, 'howifeel/index.html')

@login_required
def view_diary(request):
    return HttpResponse("View last few entries")

@login_required
def view_entry(request):
    return HttpResponse("View entry")

@login_required
def search(request):
    return HttpResponse("List of matching entries")

@login_required
def add_entry(request):
    user = request.user
    form = AddEntryForm(user=user)
    if request.method == 'POST':
        #        print("add post")
        #        if form.is_valid():
        #            print("form added")
        #            return HttpResponseRedirect('../entry_added/')

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

        # entry.save()  # looks like it is unnecessary
        return HttpResponseRedirect('../entry_added/')

    return render(request, 'howifeel/add_entry.html', { 'form': form })

@login_required
def entry_added(request):
    return render(request, 'howifeel/entry_added.html')

@login_required
def list_entries(request):
    all_entries = Entry.objects.filter(user=request.user).prefetch_related('feelings').order_by('-date')
    
    return render(request, 'howifeel/list_entries.html',
                  { 'entries': all_entries })
