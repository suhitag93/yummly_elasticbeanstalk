from django.shortcuts import render

# Create your views here.
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
import certifi
import elasticsearch
import json

index_name = "yummly_idx_3"

host = "https://search-yummly-6lgizo4lc7zcv42cdizoq3mycq.us-east-1.es.amazonaws.com"

def pull_recipes(request):
    es = Elasticsearch(host)
    if request.method == "GET":
        #pantry_contents = request.GET['pantry_items']
        pantry_contents = ['chicken', 'broccoli']

        result = []
        for item in pantry_contents:
             recipe_result = es.search(index= index_name, body={"from":0, "size": 5000, "query": {"match": {"ingredients": item}}})

        for rec in recipe_result['hits']['hits']:
            print(rec)
            result.append(["totalTimeInSeconds:",rec['_source']['totalTimeInSeconds'],'smallImageUrls:',rec['_source']['smallImageUrls'],'ingredients:',rec['_source']['ingredients'],'recipeName:',rec['_source']['recipeName']])


        #print(recipe_result)
        return HttpResponse(json.dumps(result))

# def poll_data(request):
#     while True:
#         try:
#             data_stream =    Recipes.objects.all()
#             if len(data_stream)==0:
#                 time.sleep(0.5)
#             else:
#                 recipes = []
#                 for ds in data_stream:
#                     recipes.append({"id": ds.id , "recipeName": ds.recipeName ,"ingredients": ds.ingredients ,"smallImageUrls": ds.smallImageUrls,"totalTimeInSeconds": ds.totalTimeInSeconds })
#                     response = {"new_recipes": recipes}
#                     Recipes.objects.all.delete()
#                     return HttpResponse(json.dumps(response), content_type="application/json", status= 200)
#         except:
# 			return HttpResponse(json.dumps({}),content_type="application/json",status = 200 )