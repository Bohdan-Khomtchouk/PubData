from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from SearchEngine.lib.utils import FindSearchResult
from .models import SearchQuery, Recommendation, ServerName
from .forms import SearchForm, SelectServer
from ast import literal_eval
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
import json


def home(request):
    recommendations = Recommendation.objects.all()
    return render(request, 'SearchEngine/base.html', {'recoms': recommendations})


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
    else:
        print(sum(len(d) for i, d in result.items()))
    html = render_to_string('SearchEngine/search_result.html',
                            {'all_results': result, 'error': error})
    return HttpResponse(json.dumps({'html': html}), content_type="application/json")


@csrf_exempt
@login_required
def search(request):
    search_form = SearchForm()
    servers = ServerName.objects.all()
    return render(request, 'SearchEngine/search.html',
                  {'search_form': search_form, 'servers': servers})
