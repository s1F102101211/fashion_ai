from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .forms import ChatForm
from django.utils import timezone
from fashion_ai.models import Item, Design
import openai
import environ

from .forms import StableForm
from dotenv import load_dotenv
import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

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


chat_results = ["どんなデザインにしたいですか？"]
def generate_prompt(request):
    #formに入力されている場合の処理
    if request.method == "POST":
        # ChatGPTボタン押下時
        form = ChatForm(request.POST)
        #formに入力されている場合の処理
        if form.is_valid():

            sentence = form.cleaned_data['sentence']
            chat_results.append(sentence)

            # OpenAI APIキー設定    
            env = environ.Env()
            env.read_env('.env')
            openai.api_key =env('API_KEY')
            openai.api_base = "https://api.openai.iniad.org/api/v1"
            # ChatGPT
            messages=[
                {
                    "role": "system",
                    "content": "あなたは服のデザインをユーザと一緒に考えます。考えた画像をAIで生成するためのプロンプトを日本語で出力してください"
                },
                
            ]
            for i, item in enumerate(chat_results):
                messages.append(
                    {
                        "role": "assistant" if i % 2 == 0 else "user",
                        "content": item
                    },
                )
			
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
            print(messages)
            chat_results.append(response["choices"][0]["message"]["content"])

    #formに入力されていない場合の処理->初期表示
    else:
        form = ChatForm()
    template = loader.get_template('fashion_ai/generate_prompt.html')
    context = {
        'form': form,
        'chat_results': chat_results
    }    
    return HttpResponse(template.render(context, request))

def stable(request):
    if request.method == "POST":
        # 画像生成ボタン押下時

        form = StableForm(request.POST)
        #formに入力されている場合の処理
        if form.is_valid():

            #Formのクリア
            sentence = form.cleaned_data['sentence']

            #seedの初期値
            number = 1

			#STABILITY_KEYの設定
            STABILITY_KEY = ''
            os.environ['STABILITY_KEY'] = STABILITY_KEY

            # .env ファイルから環境変数をロードする
            load_dotenv()

            # 環境変数からAPIキーを取得する
            stability_api_key = os.environ.get('STABILITY_KEY')

            # STABLITY_HOST（APIホストのURL）の設定
            # gRPCプロトコルを使用してStability.AIのサービスに接続
            os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

        
            # Stability.AIプラットフォームの生成モデルにアクセスするためのクライアントの設定
            stability_api = client.StabilityInference(
                key=os.environ['STABILITY_KEY'], # API キー
                verbose=True, # デバッグメッセージの出力するための設定
                engine="stable-diffusion-512-v2-1", # 生成に使用するエンジンの設定
            )


            # 利用可能なエンジンについては、https://platform.stability.ai/pricing を参照してください。
            #   画像サイズとステップ数に応じてクレジットが必要


            # 上記のクライアントを使用した画像生成するためのリクエスト
            answers = stability_api.generate(
                prompt=sentence,
                    #A white mixed breed of Pomeranian and Chihuahua is riding a surfboard in the style of anime
                    #prompt="生成したい画像のプロンプト",
                seed=number,
                    # 乱数生成の初期値(画像の番号)
                    # 同じシードを使用すると、生成される画像が再現可能
                steps=50, 
                    # 画像生成時に実行される推論ステップの数。
                    # デフォルトは30.
                cfg_scale=8.0, 
                    # プロンプトと生成画像の一致度を調整するためのパラメータ                         
                    # デフォルトは7.0
                width=512, 
                    # 生成画像の幅
                    # デフォルトは 512 または 1024 
                height=512,
                    # 生成画像の高さ
                    # デフォルトは 512 または 1024
                samples=1, 
                    # 生成する画像の数
                    # デフォルトは 1 です。
                sampler=generation.SAMPLER_K_DPMPP_2M 
                    # ノイズを除去するサンプラーを選択します
                    # デフォルトは k_dpmpp_2m
                )


            # Stability.AIからの応答に含まれる生成画像の処理
            for resp in answers:
                for artifact in resp.artifacts:
                    # 必要に応じて警告メッセージを表示
                    if artifact.finish_reason == generation.FILTER:
                        warnings.warn(
                        "Your request activated the API's safety filters"
                        "  and could not be processed."
                        "Please modify the prompt and try again.")
                
                    # 画像保存
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img = Image.open(io.BytesIO(artifact.binary))
                                   
                        # 保存先ディレクトリを指定します。
                        save_directory = "C:fashion_ai/static/fashion_ai/img/photo/"
                        # C:/Users/iniad/Documents/fashion_stable/fashionstable/static/fashionstable/img/

                        # 画像を指定のディレクトリに保存します。
                        file_path = os.path.join(save_directory, str(artifact.seed) + ".png")
                        print("file_path ", file_path)
                        print("file_path ", os.path.abspath(file_path))
                        img.save(file_path)


        # 生成された画像の保存パスを取得するロジックをここに追加します
        form = StableForm()
        image_path = str(artifact.seed) +".png"  # 生成された画像の実際のファイルパス

        context = {
            'form': form,
            'image_path': image_path,
        }
        number += 1
        print(number)
        return render(request, 'fashion_ai/stable.html', context)

    else: 
        form = StableForm()
        image_path =  "sample.png"  

        context = {
            'form': form,
            'image_path': image_path,
        }
        return render(request, 'fashion_ai/stable.html', context)