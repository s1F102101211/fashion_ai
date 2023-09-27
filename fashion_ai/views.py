from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import ChatForm
import openai
import environ

def index(request):
    template = loader.get_template('fashion_ai/index.html')
    context = {
        'form': ChatForm(),
    }
    return HttpResponse(template.render(context, request))

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