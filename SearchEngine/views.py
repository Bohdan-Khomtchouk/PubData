from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from SearchEngine.lib.utils import FindSearchResult
from .models import SearchQuery, Recommendation, ServerName
from .forms import SearchForm
from itertools import islice
from collections import Counter
import json


def home(request):
    recommendations = Recommendation.objects.all()
    return render(request, 'SearchEngine/base.html',
                  {})

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
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@csrf_exempt
def search_result(request, page=1):
    # query = get_object_or_404(Search, pk=pk)
    global all_result
    global founded_results
    keyword = request.POST.get('keyword')
    if keyword is None:
        # Changing the page
        page = request.GET.get('page', 1)
        paginator = Paginator(all_result, 20)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        error = None
    else:
        selected = json.loads(request.POST.get('selected'))
        # csrftoken = request.POST.get('csrfmiddlewaretoken')
        search_model = SearchQuery()
        search_model.user = request.user
        search_model.add(word=keyword, servers=list(selected))

        searcher = FindSearchResult(keyword=keyword, servers=selected, user=request.user)
        try:
            all_result = list(searcher.find_result())
            paginator = Paginator(all_result, 20)
            results = paginator.page(1)
            # cache.set('search_result', all_result, None)
            error = False
            founded_results = len(all_result)
        except ValueError as exc: 
            # invalid keyword
            error = """INVALID KEYWORD:
            Your keyword contains invalid notations!
            {}""".format(exc)
            print(error)
            results = paginator.page(0)
    index = results.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]
    if keyword is None:
        return render(request, 'SearchEngine/page_format.html',
                            {'all_results': results,
                             'error': error,
                             'founded_results': founded_results,
                             'user': request.user,
                             'page_range': page_range})
    else:
        html = render_to_string('SearchEngine/page_format.html',
                            {'all_results': results,
                             'error': error,
                             'founded_results': founded_results,
                             'user': request.user,
                             'page_range': page_range,
                             'selected_len': len(selected)})
        return HttpResponse(json.dumps({'html': html}), content_type="application/json")

@login_required()
def recom_redirect(request, keyword):
    servers = ServerName.objects.all()
    selected = {s.name: s.path for s in servers}
    searcher = FindSearchResult(keyword=keyword, servers=selected, user=request.user)
    all_result = list(searcher.find_result())
    paginator = Paginator(all_result, 20)
    results = paginator.page(1)
    error = False
    founded_results = len(all_result)
    index = results.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]
    return render(request, 'SearchEngine/page_format.html',
                            {'all_results': results,
                             'error': error,
                             'founded_results': founded_results,
                             'user': request.user,
                             'page_range': page_range,
                             'selected_len': len(selected)})

@csrf_exempt
@login_required()
def search(request):
    search_form = SearchForm()
    servers = ServerName.objects.all()
    queryset = Recommendation.objects.filter(user=request.user)

    try:
        recom_model = queryset[0]
    except IndexError:
        recomwords = []
    else:
        recomwords = Counter(recom_model.recommendations).most_common(7)
    return render(request, 'SearchEngine/search.html',
                  {'search_form': search_form,
                   'servers': servers,
                   'user': request.user,
                   'recommended_words': recomwords})
