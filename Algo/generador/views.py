from django.shortcuts import render
import json
import requests

# Create your views here.
def Index(request):
    url = requests.get("https://api.db-ip.com/v2/free/self")
    text = url.text
    data = json.loads(text)
    print(f"\n----------------------\n{data}\n----------------------\n")
    return render(request, "index.html")