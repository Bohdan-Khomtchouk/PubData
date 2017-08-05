from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.http import HttpResponse
from SearchEngine.lib.utils import FindSearchResult
from .models import SearchQuery, Recommendation, ServerName
from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    recommendations = Recommendation.objects.all()
    return render(request, 'SearchEngine/base.html', {'recoms': recommendations})


def user_profile(request):
    pass


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/searchengine')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@csrf_exempt
def search_result(request):
    # query = get_object_or_404(Search, pk=pk)
    keyword = request.POST.get('keyword')
    selected = json.loads(request.POST.get('selected'))
    # csrftoken = request.POST.get('csrfmiddlewaretoken')
    search_model = SearchQuery()
    search_model.user = request.user
    search_model.add(word=keyword, servers=list(selected))

    searcher = FindSearchResult(keyword=keyword, servers=selected)
    try:
        result = searcher.find_result()
        error = False
    except ValueError as exc:
        # invalid keyword
        error = """INVALID KEYWORD:
        Your keyword contains invalid notations!
        {}""".format(exc)
        result = []
        print(error)
    finally:
        founded_results = sum(len(d['data']) for d in result.values())
        print("{} results founded".format(founded_results))
    html = render_to_string('SearchEngine/search_result.html',
                            {'all_results': result,
                             'error': error,
                             'founded_results': founded_results,
                             'user': request.user})
    return HttpResponse(json.dumps({'html': html}), content_type="application/json")


@csrf_exempt
@login_required()
def search(request):
    search_form = SearchForm()
    servers = ServerName.objects.all()
    return render(request, 'SearchEngine/search.html',
                  {'search_form': search_form, 'servers': servers})
