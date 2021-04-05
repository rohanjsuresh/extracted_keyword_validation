from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.apps import apps
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

User_Validation = apps.get_model('keyword_relation', 'User_Validation')
Keyword_Pages = apps.get_model('keyword_relation', 'Keyword_Pages')

# Create your views here.
@staff_member_required
def admin_tool(request):

    # Get all values from user_validation
    all_inputs = User_Validation.objects.all()

    data_pos = []
    data_neg = []
    labels = [] 

    # key: keyword
    # val: [num_pos, num_neg]
    label_data_map = {}

    for val in all_inputs:
        if val.domainness_belongs_to_domain == -1:
            continue
        else:
            if val.main_keyword not in label_data_map.keys():
                label_data_map[val.main_keyword] = [0,0]
            if val.domainness_belongs_to_domain == 1:
                temp = label_data_map[val.main_keyword]
                temp[0] += 1
                label_data_map[val.main_keyword] = temp
            elif val.domainness_belongs_to_domain == 0:
                temp = label_data_map[val.main_keyword]
                temp[1] += 1
                label_data_map[val.main_keyword] = temp

    # put into arrays
    for label in label_data_map.keys():
        labels.append(label)
        data_pos.append(label_data_map[label][0])
        data_neg.append(label_data_map[label][1])

    context = {}
    # context["labels"] = labels
    # context["data"] = data_pos

    return render(request, 'admin_extended/admin_tool.html', context)



def populate_chart(request):
    # Get all values from user_validation
    all_inputs = User_Validation.objects.all()

    data_pos = []
    data_neg = []
    labels = [] 

    # key: keyword
    # val: [num_pos, num_neg]
    label_data_map = {}

    for val in all_inputs:
        if val.domainness_belongs_to_domain == -1:
            continue
        else:
            if val.main_keyword not in label_data_map.keys():
                label_data_map[val.main_keyword] = [0,0]
            if val.domainness_belongs_to_domain == 1:
                temp = label_data_map[val.main_keyword]
                temp[0] += 1
                label_data_map[val.main_keyword] = temp
            elif val.domainness_belongs_to_domain == 0:
                temp = label_data_map[val.main_keyword]
                temp[1] += 1
                label_data_map[val.main_keyword] = temp

    # put into arrays
    for label in label_data_map.keys():
        labels.append(label)
        data_pos.append(label_data_map[label][0])
        data_neg.append(label_data_map[label][1])

    return JsonResponse(data={
        'labels': labels,
        'data_pos': data_pos,
        'data_neg': data_neg,
    })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # print(myfile.name)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        new_keywords = []
        for line in myfile:
            new_keywords.append(line.decode("utf-8").rstrip("\n"))

        insert_new_keywords(new_keywords)

        uploaded_file_url = fs.url(filename)
        return render(request, 'admin_extended/admin_tool.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'admin_extended/admin_tool.html')


def insert_new_keywords(new_keywords):
    old_vals = list(User_Validation.objects.values_list('main_keyword', flat=True).distinct())

    # Initialize new keywords idx array
    new_vals = [x.lower() for x in new_keywords]
    idx = [i for i in range(len(new_vals))] 

    # Dupliates test
    idx_pass = []
    for val in idx:
        if new_vals[val] not in old_vals:
            idx_pass.append(val)
    idx = idx_pass

    # Create Acronym
    acronyms_old = []
    for val in old_vals:
        val_split = val.split()
        if len(val_split) > 1:
            acronyms_old.append("".join(e[0] for e in val_split))


    # Acronym test
    idx_pass = []
    for val in idx:
        if new_vals[val] not in acronyms_old:
            idx_pass.append(val)
            
    idx = idx_pass

    # Stemming Test
    porter = PorterStemmer()
    stemmed = []
    for val in old_vals:
        stemmed.append(porter.stem(val))
        
    idx_pass = []
    for val in idx:
        if porter.stem(new_vals[val]) not in stemmed:
            idx_pass.append(val)
            
    idx = idx_pass


    # Lemmatization Test
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized = []

    for val in old_vals:
        lemmatized.append(wordnet_lemmatizer.lemmatize(val))
        
    idx_pass = []
    for val in idx:
        if wordnet_lemmatizer.lemmatize(new_vals[val]) not in lemmatized:
            idx_pass.append(val)
            
    idx = idx_pass

    # insert into model
    # set wiki_definition to ""
    # matched_with = "N/A"
    # google_graph_embedding = ""
    # wiki_path = ""
    for val in idx_pass:
        print(new_vals[val])
        new_val = Keyword_Pages(keyword = new_vals[val], matched_with = "N/A", wiki_definition = "", google_graph_embedding = "", wiki_path = "")
        new_val.save()