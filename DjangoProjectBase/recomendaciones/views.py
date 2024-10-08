from django.shortcuts import render
from django.http import HttpResponse
from movie.models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
import os
import json
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

_ = load_dotenv('/Users/david/Taller3_PI1/api_keys.env')
client = OpenAI(api_key=os.environ.get('api_key_3_3'),)

with open('/Users/david/Taller3_PI1//movie_descriptions_embeddings.json', 'r') as file:
    file_content = file.read()
    movies = json.loads(file_content)
    
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recommend(user_input):
    emb = get_embedding(user_input)
    sim = []
    
    for movie in movies:
        sim.append(cosine_similarity(emb, movie['embedding']))
    
    sim = np.array(sim)
    
    idx = np.argmax(sim)
    
    return movies[idx]

def recommendations(request):
    search_term = request.GET.get('searchMovie', '')
    recommended_movie = None
    
    if search_term:
        recommended_movie = recommend(search_term)
    
    return render(request, 'recomendaciones/recommendations.html', {
        'searchTerm': search_term,
        'recommended_movie': recommended_movie
    })