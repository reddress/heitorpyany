from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Diary, Entry
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

        
        print(request.user)
        print(request.POST['diary'])
        
        print(request.POST['text'])
        print(request.POST['feelings'])
        print(request.POST['energy'])
        print(request.POST['mood'])

        if request.POST['diary'] == '':
            diary = Diary.objects.get(user=user, name="Untitled")
        else:
            diary = Diary.objects.get(user=user, pk=int(request.POST['diary']))

        title = request.POST['title']
        text = request.POST['text']

        # FIXME split by comma, strip whitespace, check if feeling exists,
        # if not, add to list
        feelings = request.POST['feelings']
        energy = int(request.POST['energy'])
        mood = int(request.POST['mood'])

        entry = Entry(user=user, diary=diary, title=title, text=text,
                      # FIXME feelings = ???
                      energy=energy, mood=mood)
        entry.save()
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
