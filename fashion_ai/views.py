from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .forms import ChatForm
from django.utils import timezone
from fashion_ai.models import Item, Design
import openai
import environ

def index(request):
    template = loader.get_template('fashion_ai/index.html')
    context = {
        'form': ChatForm(),
    }
    return HttpResponse(template.render(context, request))

def start(request):
	return render(request, 'fashion_ai/start.html')

def home(request):
	return render(request, 'fashion_ai/home.html')

def select(request):
	context = {
		"tops" : Item.objects.filter(category1="トップス"),
		"bottoms" : Item.objects.filter(category1="ボトムス"),
		"outers" : Item.objects.filter(category1="アウター"),
		"others" : Item.objects.exclude(category1__in=["トップス","ボトムス","アウター"]),
	}
	return render(request, 'fashion_ai/select.html', context)

def prompt(request, id):
	try:
		item = Item.objects.get(pk=id)
	except Item.DoesNotExist:
		raise Http404()
	if request.method == 'POST':
		design=Design()
		design.item_id = request.POST['item_id']
		design.category1 = request.POST['category1']
		design.category2 = request.POST['category2']
		design.title = request.POST['title']
		design.img = request.POST['img']
		design.save()
		return redirect(preview, design.id)
	
	context = {
		"item" : item,
	}
	return render(request, 'fashion_ai/prompt.html', context)

def preview(request, id):
	try:
		design = Design.objects.get(pk=id)
	except Design.DoesNotExist:
		raise Http404()
	
	context = {
		"design" : design
	}
	return render(request, 'fashion_ai/preview.html', context)

def original(request):
	context = {
		"tops" : Design.objects.filter(category1="トップス"),
		"bottoms" : Design.objects.filter(category1="ボトムス"),
		"outers" : Design.objects.filter(category1="アウター"),
		"others" : Design.objects.exclude(category1__in=["トップス","ボトムス","アウター"]),
	}
	return render(request, 'fashion_ai/original.html', context)

def update_design(request, id):
	try:
		design = Design.objects.get(pk=id)
	except Design.DoesNotExist:
		raise Http404()
	if request.method == 'POST':
		design.title = request.POST['title']
		design.save()
		return redirect(original)
	
	context = {
        "design" : design,
		"tops" : Design.objects.filter(category1="トップス"),
		"bottoms" : Design.objects.filter(category1="ボトムス"),
		"outers" : Design.objects.filter(category1="アウター"),
		"others" : Design.objects.exclude(category1__in=["トップス","ボトムス","アウター"]),
    }
	return render(request, 'fashion_ai/original.html', context)

def delete_design(request, id):
    try:
        design = Design.objects.get(pk=id)
    except Design.DoesNotExist:
        raise Http404()
    design.delete()
    return redirect(original)

def collection(request):
	return render(request, 'fashion_ai/collection.html')

def gallery(request):
	return render(request, 'fashion_ai/gallery.html')


def data(request):
	if request.method == 'POST':
		item=Item()
		item.category1 = request.POST['category1']
		item.category2 = request.POST['category2']
		item.img = request.POST['img']
		item.save()
		return redirect(data)

	context = {
		"tops" : Item.objects.filter(category1="トップス"),
		"bottoms" : Item.objects.filter(category1="ボトムス"),
		"outers" : Item.objects.filter(category1="アウター"),
		"others" : Item.objects.exclude(category1__in=["トップス","ボトムス","アウター"]),
	}
	return render(request, 'fashion_ai/data.html', context)

def update_item(request, id):
	try:
		item = Item.objects.get(pk=id)
	except Item.DoesNotExist:
		raise Http404()
	if request.method == 'POST':
		item.category1 = request.POST['category1']
		item.category2 = request.POST['category2']
		item.img = request.POST['img']
		item.save()
		return redirect(data)
	
	context = {
        "item" : item,
		"tops" : Item.objects.filter(category1="トップス"),
		"bottoms" : Item.objects.filter(category1="ボトムス"),
		"outers" : Item.objects.filter(category1="アウター"),
		"others" : Item.objects.exclude(category1__in=["トップス","ボトムス","アウター"]),
    }
	return render(request, 'fashion_ai/data.html', context)

def delete_item(request, id):
    try:
        item = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404()
    item.delete()
    return redirect(data)


def generate_prompt(request):
    chat_results = ""
    #formに入力されている場合の処理
    if request.method == "POST":
        # ChatGPTボタン押下時

        form = ChatForm(request.POST)
        #formに入力されている場合の処理
        if form.is_valid():

            sentence = form.cleaned_data['sentence']

            # OpenAI APIキー設定    
            env = environ.Env()
            env.read_env('.env')
            openai.api_key =env('API_KEY')
            openai.api_base = "https://api.openai.iniad.org/api/v1"
            # ChatGPT
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "日本語で応答してください"
                    },
                    {
                        "role": "user",
                        "content": sentence
                    },
                ],
            )

            chat_results = response["choices"][0]["message"]["content"]

    #formに入力されていない場合の処理->初期表示
    else:
        form = ChatForm()
    template = loader.get_template('fashion_ai/generate_prompt.html')
    context = {
        'form': form,
        'chat_results': chat_results
    }    
    return HttpResponse(template.render(context, request))
