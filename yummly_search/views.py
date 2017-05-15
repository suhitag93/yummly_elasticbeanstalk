from django.shortcuts import render

# Create your views here.
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
import certifi
import elasticsearch
import json

index_name = "yummly_idx"

host = "https://search-pantry2pan-7smzvxcni52n7uhnvtrwzrhj2q.us-east-1.es.amazonaws.com"

def pull_recipes(request):
    es = Elasticsearch(host)
    if request.method=='GET':
        pantry_items = [request.GET['pantry_items']];
        #pantry_contents=['chicken']
        result = []
        recipe_result=[]

        for item in pantry_items:
            recipe_result = es.search(index= index_name, body={"from":0, "size": 5000, "query": {"match": {"ingredients": item }}})
            for rec in recipe_result['hits']['hits']:
                print(rec)
                result.append(rec)
    #             result.append({"totalTimeInSeconds:",rec['_source']['totalTimeInSeconds'],
    #                           'smallImageUrls:',rec['_source']['smallImageUrls'],'ingredients:',rec['_source']['ingredients'],'recipeName:',rec['_source']['recipeName']})
    else:
        pantry_items=["chicken","broccoli", "asparagus"]
        result = []
        recipe_result=[]
        for item in pantry_items:
            recipe_result =es.search(index= index_name, body={"from":0, "size": 5000, "query": {"match": {"ingredients": item}}})
            print(recipe_result)
            for rec in recipe_result['hits']['hits']:
                result.append(rec)
    return HttpResponse(json.dumps(result,))
