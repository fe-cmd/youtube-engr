import requests
import argparse
import httplib2
import http.client as httplib
import os
import random
import time
import nlpcloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


import google.oauth2.credentials
import google_auth_oauthlib.flow
from django.shortcuts import render, redirect
from imp import reload
from django.http import HttpResponse, JsonResponse
from pytube import YouTube
from django.contrib import messages
# Create your views here.
from isodate import parse_duration
from django.conf import settings
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import WebVTTFormatter
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from .models import Filters
from .filters import FiltersFilter
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

def ytb_down(request):
    return render(request, "youtube_app/base.html")

def ytb_download(request):
    url = request.GET.get('url')
    obj = YouTube(url)
    resolutions = []
    strm_all = obj.streams.all()
    for i in strm_all:
        resolutions.append(i.resolution)
    resolutions = list(dict.fromkeys(resolutions))
    
    
    embed_link = url.replace("watch?v=", "embed/")

    return render(request, "youtube_app/videos.html", {'rsl': resolutions, 'embd':embed_link})
 
 

def get_youtube_video_id(url):
    from urllib.parse import urlparse,parse_qs

    if url.startswith(('youtu','www')):
            url = 'http://' + url

    query = urlparse(url)

    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError

def start(request):
   url_1 = request.GET.get('url_s')
   vid_id = get_youtube_video_id(url_1)
   print(url_1)
   transcripts = YouTubeTranscriptApi.list_transcripts(vid_id)
   base_lang = "en"
   target_lang = "es"
   #print(transcripts)
   base_obj = transcripts.find_transcript([base_lang])
   base_trans = base_obj.fetch()

   fmt = TextFormatter()
   base_txt = fmt.format_transcript(base_trans)
   print("writing {} transcript....".format(base_lang), end="")
   with open("static/{}_transcript.txt".format(base_lang), "w") as f:
      f.write(base_txt)
   print("DONE")
   
   #translate to another language
   if base_obj.is_translatable:
      target_trans = base_obj.translate(target_lang).fetch()
   else:
      print("CAN NOT translate transcript is {}".format(target_lang))
      quit()

   print(target_trans)

   #print our wanted or target language
   wanted_txt = fmt.format_transcript(target_trans)
   print("writing {} transcript....".format(target_lang), end="")
   with open("static/{}_transcript.txt".format(target_lang), "w") as f:
      f.write(wanted_txt)

   #get subtitles for the YT Views
   fst = WebVTTFormatter()
   target_subs = fst.format_transcript(target_trans)
   print("writing {} transcript....".format(target_lang), end="")
   with open("static/{}_transcript.vtt".format(target_lang), "w") as f:
      f.write(target_subs)
   return render(request, 'youtube_app/play_video.html', {'sub': base_txt})


# defining function
def youtube(request):
  
    # checking whether request.method is post or not
    if request.method == 'POST':
        
        # getting link from frontend
        link = request.POST['link']
        video = YouTube(link)
  
        # setting video resolution
        stream = video.streams.get_lowest_resolution()
        path = 'C:/Users/GB/Desktop/'
        # downloads video
        stream = stream.download(path)


  
        # returning HTML page
    return render(request, 'youtube_app/downloads.html', {'stream':stream, 'msg':'Video downloaded \
            kindly check your computer Desktop window to access it Thanks.'})
    
def summarise(text):
     stopWords = set(stopwords.words("english"))
     words = word_tokenize(text)
     # Creating a frequency table to keep the
     # score of each word
     freqTable = dict()
     for word in words:
	     word = word.lower()
	     if word in stopWords:
		     continue
	     if word in freqTable:
		     freqTable[word] += 1
	     else:
		     freqTable[word] = 1
     # Creating a dictionary to keep the score
     # of each sentence
     sentences = sent_tokenize(text)
     sentenceValue = dict()
            
     for sentence in sentences:
    	 for word, freq in freqTable.items():
		     if word in sentence.lower():
			     if sentence in sentenceValue:
				            sentenceValue[sentence] += freq
			     else:
				     sentenceValue[sentence] = freq
            
     sumValues = 0
     for sentence in sentenceValue:
    	 sumValues += sentenceValue[sentence]

     # Average value of a sentence from the original text

     average = int(sumValues / len(sentenceValue))
            
      # Storing sentences into our summary.
     summary = ''
     for sentence in sentences:
	     if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.7 * average)):
		     summary += " " + sentence
     return summary

def summarise1(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
      # Creating a frequency table to keep the
      # score of each word
    freqTable = dict()
    for word in words:
	    word = word.lower()
	    if word in stopWords:
		    continue
	    if word in freqTable:
		    freqTable[word] += 1
	    else:
		    freqTable[word] = 1
    # Creating a dictionary to keep the score
    # of each sentence
    sentences = sent_tokenize(text)
    sentenceValue = dict()
            
    for sentence in sentences:
    	for word, freq in freqTable.items():
		    if word in sentence.lower():
			    if sentence in sentenceValue:
				    sentenceValue[sentence] += freq
			    else:
				    sentenceValue[sentence] = freq
            
    sumValues = 0
    for sentence in sentenceValue:
    	sumValues += sentenceValue[sentence]

    # Average value of a sentence from the original text

    average = int(sumValues / len(sentenceValue))
            
    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
	    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.7 * average)):
		    summary += " " + sentence
    return summary
     
def search_ytb(request):
    videos = []
    query = request.POST['search']
    key = settings.NLP_API_KEY

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : query,
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 10,
            'type' : 'video',
            'order' : 'relevance',
            'videoCaption' : 'closedCaption',
            'relevanceLanguage': 'en',
            'videoDuration': 'medium',
            'videoDefinition': 'standard',
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
            
        vid = f'https://www.youtube.com/watch?v={ video_ids[0] }'
        if request.POST['submit'] == 'lucky':
            return redirect(vid,'embed/')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 10
        }
        
        r = requests.get(video_url, params=video_params)

        results = r.json()['items']
        kw = []
        for result in results:
            transcripts = YouTubeTranscriptApi.list_transcripts(result["id"])
            base_lang = "en"
            #print(transcripts)
            base_obj = transcripts.find_transcript([base_lang])
            base_trans = base_obj.fetch()
            fmt = TextFormatter()
            base_txt = fmt.format_transcript(base_trans)
            res1 = summarise(base_txt)
            
            client = nlpcloud.Client("finetuned-gpt-neox-20b", key, gpu=True, lang="en")
            res_3 = client.kw_kp_extraction(
                res1
            )
            kw.append(res_3)
            
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'video': f'https://www.youtube.com/embed/{ result["id"] }',
                'url1' : 'youtube_app/subtitle.html'

             }
             
             
            videos.append(video_data)
            videos.append(res1)

        

    context = {
        'videos' : videos,
        'query':query, 
        'kw':kw,
    }
    
    messages.info(
                    request, f'Search results uploading in progress.......success!!!')
    
    return render(request, 'youtube_app/downloads1.html', context)



             
def subtitle_ytb(request):
    query = request.POST['search3']

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : query,
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 5,
            'type' : 'video',
            'order' : 'relevance',
            'videoCaption' : 'closedCaption',
            'relevanceLanguage': 'en',
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
            
        vid = f'https://www.youtube.com/watch?v={ video_ids[0] }'
        if request.POST['submit'] == 'lucky':
            return redirect(vid,'embed/')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 5
        }
        
        

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']
        for result in results:
             transcripts = YouTubeTranscriptApi.list_transcripts(result["id"])
             base_lang = "en"
             #print(transcripts)
             base_obj = transcripts.find_transcript([base_lang])
             base_trans = base_obj.fetch()

             fmt = TextFormatter()
             base_txt = fmt.format_transcript(base_trans)
              
             messages.info(
                    request, f'Search subtitles results uploading in progress.......success!!!')
             
             return render(request, 'youtube_app/subtitle.html', {'sub': base_txt})
             
def search_ytb1(request):
    channels = []
    query = request.POST['search1']

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        channel_url = 'https://www.googleapis.com/youtube/v3/channels'

        search_params = {
            'part' : 'snippet',
            'q' : query,
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 25,
            'type' : 'channel'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        channel_ids = []
        for result in results:
            channel_ids.append(result['id']['channelId'])
            
        chan = f'https://www.youtube.com/channel/{ channel_ids[0] }'
        if request.POST['submit'] == 'lucky':
            return redirect(chan, 'embed/')

        
        channel_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(channel_ids),
            'maxResults' : 25
        }
        
        r1 = requests.get(channel_url, params=channel_params)

        results1 = r1.json()['items']
       
        for result in results1:
            channel_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/channel/{ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
            }

            channels.append(channel_data)

    context = {
        'query':query,
        'channels': channels,
    }
    
    return render(request, 'youtube_app/channels.html', context)

def search_ytb2(request):
    playlists = []
    query = request.POST['search2']

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        playlist_url = 'https://www.googleapis.com/youtube/v3/playlists'

        search_params = {
            'part' : 'snippet',
            'q' : query,
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 10,
            'type' : 'playlist'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']
        
        playlist_ids = []
        for result in results:
            playlist_ids.append(result['id']['playlistId'])

            
        play = f'https://www.youtube.com/playlist/{ playlist_ids[0] }'
        if request.POST['submit'] == 'lucky':
            return redirect(play, 'embed/')

        
        playlist_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(playlist_ids),
            'maxResults' : 10
        }
        
        r2 = requests.get(playlist_url, params=playlist_params)

        results2 = r2.json()['items']
       
        for result in results2:
            playlist_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/playlist/{ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
            }

            playlists.append(playlist_data)

    context = {
        'query':query,
        'playlists': playlists,
    }
    
    return render(request, 'youtube_app/playlist.html', context)

def show_filters(request):
    context = {} 
    filter_params = FiltersFilter(
        request.GET,
        queryset=Filters.objects.all()
    )
    
    context['filter_params'] = filter_params
    
    return render(request, 'youtube_app/search_filter.html', context=context)

def machine_models(request):
    return render(request, 'youtube_app/Nlp-Ai.html')

def ai_ml_gen(request):
  context = []
  if request.method == 'GET':
    ml = request.GET['nlp']
    key = settings.NLP_API_KEY
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'part' : 'snippet',
        'q' : ml,
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 10,
        'type' : 'video',
        'order' : 'relevance',
        'videoCaption' : 'closedCaption',
        'relevanceLanguage': 'en',
        'videoDuration': 'medium',
        'videoDefinition': 'standard',
    }

    r = requests.get(search_url, params=search_params)

    results = r.json()['items']

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])
            
    vid = f'https://www.youtube.com/watch?v={ video_ids[0] }'
    
    if request.GET['submit_m'] == 'lucky':
        return redirect('ai_ml_gen')

    video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 10
        }
        
    r = requests.get(video_url, params=video_params)

    results = r.json()['items']
    kw = []
    outs = []
    for result in results:
        transcripts = YouTubeTranscriptApi.list_transcripts(result["id"])
        base_lang = "en"
        #print(transcripts)
        base_obj = transcripts.find_transcript([base_lang])
        base_trans = base_obj.fetch()
        fmt = TextFormatter()
        base_txt = fmt.format_transcript(base_trans)
        res1 = summarise(base_txt)
        outs.append(res1)
    client = nlpcloud.Client("finetuned-gpt-neox-20b", key, gpu=True, lang="en")
    for out in outs:
      res_3 = client.kw_kp_extraction(
              out
              )
      kw.append(res_3)
        
    
    if  ml == '':
        messages.error(request, 'Error ---> please fill in your desired details to get results')
        return render(request, 'youtube_app/Nlp-Ai.html')
   
    else:
      client = nlpcloud.Client("fast-gpt-j", key, gpu=True, lang="en")
      res = client.article_generation(
               ml
            ) 
    res1 = summarise1(res)
    client = nlpcloud.Client("finetuned-gpt-neox-20b", key, gpu=True, lang="en")
    res_2 = client.kw_kp_extraction(
        res1
    ) 
           
    print(res_2)   
    messages.success(request, 'results generated successfully!!! cheers')
    
    context = {
        'kw':kw,
        'res_2':res_2,
    }
    
    return render(request, 'youtube_app/Nlp-Ai.html', context)

def match_nlp(request):
     if request.method == 'GET':
       txt1 = request.GET['txt1']
       txt2 = request.GET['txt2']
       key = settings.NLP_API_KEY
    
       if request.GET['submit_n'] == 'lucky':
           return redirect('ai_ml_gen')
       
       client = nlpcloud.Client("paraphrase-multilingual-mpnet-base-v2", key, gpu=False)
       res = client.semantic_similarity([
             txt1,
             txt2    
             ])
       print(res)
       
       return render(request, 'youtube_app/Nlp-Ai.html', {'match': res})

       
       