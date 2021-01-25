from django.shortcuts import render
from .models import Keyword_Pages
from .models import Pairs_In_Circulation
from .models import Correct_Pairs
from .models import Incorrect_Pairs
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls.static import static
import os
from django.conf import settings
import numpy as np
import random
from gensim.models import Word2Vec
import wikipedia


# Create your views here.

def home(request):
    return render(request, 'keyword_relation/index.html', {})


def keyword_pages(request):
    #render spreadsheet
    all_keywords = Keyword_Pages.objects.all()

    context = {}
    keyword_str = ""
    wikipedia_content_str = ""
    related_keywords_str = ""
    first = True

    for keywords in all_keywords:
        if first:
            keyword_str += keywords.keyword 
        else: 
            keyword_str += "|" + keywords.keyword

        # https://stackoverflow.com/questions/25946692/wikipedia-disambiguation-error
        try:
            if first:
                wikipedia_content_str += wikipedia.summary(keywords.keyword, sentences=1)
            else: 
                wikipedia_content_str += "|" + wikipedia.summary(keywords.keyword, sentences=1)

        except wikipedia.DisambiguationError as e:
            s = e.options[0]
            if first:
                wikipedia_content_str += wikipedia.summary(s, sentences=1)
            else: 
                wikipedia_content_str += "|" + wikipedia.summary(s, sentences=1)

        if first:
            related_keywords_str += keywords.matched_with 
        else: 
            # Different delimeter used because DB uses '|' and ',' as delimeter
            related_keywords_str += "&" + keywords.matched_with

        first = False

    context["keywords"] = keyword_str 
    context["wikipedia_content"] = wikipedia_content_str
    context["related_keywords"] = related_keywords_str

    print(keyword_str)
    print(related_keywords_str)

    return render(request, 'keyword_relation/keyword_pages_default.html', context)

def verify_relationship_tool(request):
    # get random row from relationship in circulation table
    rand_obj = Pairs_In_Circulation.objects.order_by('?').first()

    keyword_fst = rand_obj.keyword_fst
    keyword_snd = rand_obj.keyword_snd

    print(keyword_fst)
    print(keyword_snd)

    context = {"keyword_fst":keyword_fst, "keyword_snd":keyword_snd}

    title_str = ""
    abstract_str = ""
    linked_title = ""

    # read arxiv 
    titles_path = os.path.join(settings.STATIC_ROOT,'../arxiv_data/arxiv_titles.npy')
    abstracts_path = os.path.join(settings.STATIC_ROOT,'../arxiv_data/arxiv_abstracts.npy')

    titles = np.load(titles_path, mmap_mode='r')
    abstracts = np.load(abstracts_path, mmap_mode='r')

    print("loaded")

    found = 0
    first_title = True
    first_abstract = True
    for i in range(200000):
        idx = random.randint(0, len(titles)-1)
        if keyword_fst in titles[idx] and keyword_snd in titles[idx]:
            if first_title:
                title_str += titles[idx]
                first_title = False
            else:
                title_str += "|" + titles[idx]

            found += 1

        idx = random.randint(0, len(titles)-1)
        if keyword_fst in abstracts[idx] and keyword_snd in abstracts[idx]:
            if first_abstract:
                abstract_str += abstracts[idx]
                linked_title += titles[idx]
                first_abstract = False
            else:
                abstract_str += "|" + abstracts[idx]
                linked_title += "|" + titles[idx]
            
            found += 1

        if found >= 5:
            break

    print("FOUND: ", found)

    context["title_str"] = title_str
    context["abstract_str"] = abstract_str
    context["linked_title"] = linked_title

    print(title_str)
    print(abstract_str)
    print(linked_title)

    # models
    model_path = os.path.join(settings.STATIC_ROOT,'../models/related_keywords_graph_embedding.model')
    model = Word2Vec.load(model_path)

    related_fst = find_similar_keywords(model, keyword_fst)
    related_snd = find_similar_keywords(model, keyword_snd)

    context["related_fst"] = related_fst
    context["related_snd"] = related_snd

    print(related_fst)
    print(related_snd)

    return render(request, 'keyword_relation/keyword_rel_tool.html', context)


# function to get related keywords
def find_similar_keywords(model, x):
    output = ""
    first = True
    try:
        for node, _ in model.wv.most_similar(x):
            if first:
                output += node
                first = False
            else:
                output += "|" + node
    except:
        print(x, "not in graph")
    return output

def add_entry(request):
    
    # get user response
    user_response = request.POST.get("user_input").lower()

    # get keywords
    keyword_fst = request.POST.get("keyword_fst_response").lower()
    keyword_snd = request.POST.get("keyword_snd_response").lower()

    if user_response == "yes":

        # check to see if keywords is in table
        num_results = len(Pairs_In_Circulation.objects.filter(keyword_fst=keyword_fst, keyword_snd=keyword_snd))

        # if no results insert new element into table
        if num_results == 0:
            new_record = Pairs_In_Circulation(keyword_fst=keyword_fst, keyword_snd=keyword_snd, correct_match_count=1, incorrect_match_count=0, times_classified=1)
            new_record.save()
            new_record = Pairs_In_Circulation(keyword_fst=keyword_snd, keyword_snd=keyword_fst, correct_match_count=1, incorrect_match_count=0, times_classified=1)
            new_record.save()
        else:
            update_record = Pairs_In_Circulation.objects.get(keyword_fst=keyword_fst, keyword_snd=keyword_snd)
            update_record.times_classified += 1
            update_record.correct_match_count += 1
            update_record.save()
            update_record = Pairs_In_Circulation.objects.get(keyword_fst=keyword_snd, keyword_snd=keyword_fst)
            update_record.times_classified += 1
            update_record.correct_match_count += 1
            update_record.save()

    elif user_response == "no":

        # check to see if keywords is in table
        num_results = len(Pairs_In_Circulation.objects.filter(keyword_fst=keyword_fst, keyword_snd=keyword_snd))

        # if no results insert new element into table
        if num_results == 0:
            new_record = Pairs_In_Circulation(keyword_fst=keyword_fst, keyword_snd=keyword_snd, correct_match_count=0, incorrect_match_count=1, times_classified=1)
            new_record.save()
            new_record = Pairs_In_Circulation(keyword_fst=keyword_snd, keyword_snd=keyword_fst, correct_match_count=0, incorrect_match_count=1, times_classified=1)
            new_record.save()
        else:
            update_record = Pairs_In_Circulation.objects.get(keyword_fst=keyword_fst, keyword_snd=keyword_snd)
            update_record.times_classified += 1
            update_record.incorrect_match_count += 1
            update_record.save()
            update_record = Pairs_In_Circulation.objects.get(keyword_fst=keyword_snd, keyword_snd=keyword_fst)
            update_record.times_classified += 1
            update_record.incorrect_match_count += 1
            update_record.save()

    return verify_relationship_tool(request)

def dynamic_lookup_view(request, keyword):
    obj = Keyword_Pages.objects.get(keyword=keyword)
    context = {
        "keyword":obj.keyword.capitalize(),
        "matched":obj.matched_with,
    }

    # models
    model_path = os.path.join(settings.STATIC_ROOT,'../models/related_keywords_graph_embedding.model')
    model = Word2Vec.load(model_path)

    related_fst = find_similar_keywords(model, obj.keyword.lower())

    context["related_fst"] = related_fst

    return render(request, 'keyword_relation/keyword_page.html', context)

def search(request):
    search_input = request.POST.get("search_input")
    return dynamic_lookup_view(request, search_input)