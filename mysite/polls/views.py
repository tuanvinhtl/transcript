from django.shortcuts import render
from .forms import AudioFileForm
import requests
import time
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Do something after saving the file
    else:
        form = AudioFileForm()
    return render(request, 'polls/upload.html', {'form': form})

def make_fetch_request(url, headers, method='GET', data=None):
    if method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    else:
        response = requests.get(url, headers=headers)
    return response.json()

@csrf_exempt
def transcription_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
           # Extract audio URL from request payload
        audio_url = data.get('audio_url')

        # Set a default value if audio_url is None or empty
        if not audio_url:
            audio_url = ""

        gladia_key = "89b90f8f-5880-4f19-a5b6-a25306a064d4"
        gladia_url = "https://api.gladia.io/v2/transcription/"
        
        request_data = {"audio_url": audio_url}
        headers = {
            "x-gladia-key": gladia_key,
            "Content-Type": "application/json"
        }

        print("- Sending initial request to Gladia API...")
        initial_response = make_fetch_request(gladia_url, headers, 'POST', request_data)

        print("Initial response with Transcription ID:", initial_response)
        result_url = initial_response.get("result_url")

        if result_url:
            while True:
                print("Polling for results...")
                poll_response = make_fetch_request(result_url, headers)
                
                if poll_response.get("status") == "done":
                    # transcription_text = poll_response.get("result", {}).get("transcription", {}).get("full_transcript")
                    # return render(request, 'polls/transcription.html', {'transcription_text': transcription_text})
                    return JsonResponse(poll_response.get("result", {}))
                else:
                    print("Transcription status:", poll_response.get("status"))
                time.sleep(1)

    else:
        return HttpResponseNotAllowed(['GET'])