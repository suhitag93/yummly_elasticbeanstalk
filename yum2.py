import yummly
import json
import requests
from elasticsearch import Elasticsearch
from yummly import Client


q = "paneer"

mapping = {"mapping" : {
        "recipe":{

        "properties": {
             "recipeName": {
              "type" : "string"
            },

            "smallImageUrls":{
               "type" : "string"
            },
             "totalTimeInSeconds":{
                "type" : "number"
            },
            "ingredients":{
                "type" : "string"
            },

            "sourceURL" :{
                "type" : "string"
            },
            "cuisine":{
                "type" : "string"
            }

        }
      }
    }
}

clt = Client(api_id="6aa3b3c5", api_key="98f091eede210875e3db43249b670de4",timeout=5.0,retries=0)


maxRes = 70
search = clt.search(q,maxResult=maxRes)

host = "https://search-yummly-recipes-jim5fnxd4z4p4pbswyajetxtka.us-east-1.es.amazonaws.com"

es =  Elasticsearch(host)

idx_name = "yummly_idx"

es.indices.create(index=idx_name,body=mapping, ignore=400)

#make a for loop here till maxResult

for i in range(0,maxRes):
    try:
        match = search.matches[i]
        recipe = clt.recipe(match.id)
        if (recipe.attributes['cuisine']):
            r = recipe.attributes['cuisine']
        else:
            r = ["u'Unknown'"]
        print(recipe.attributes['cuisine'])
        print(q,match.id,match.recipeName,match.ingredients, match.smallImageUrls, recipe.attributes['cuisine'],recipe.source.sourceRecipeUrl )
        es.index(index=idx_name,id=match.id,doc_type="recipe",body={"recipeName":match.recipeName, "ingredients":match.ingredients,
            "smallImageUrls":match.smallImageUrls, "totalTimeInSeconds":match.totalTimeInSeconds,"sourceURL":recipe.source.sourceRecipeUrl, "cuisine":r});
    except Exception as e:
        print("ERROR: "+ str(e))
        r=["u'Unknown'"]
        es.index(index=idx_name,id=match.id,doc_type="recipe",body={"recipeName":match.recipeName, "ingredients":match.ingredients,
            "smallImageUrls":match.smallImageUrls, "totalTimeInSeconds":match.totalTimeInSeconds,"sourceURL":recipe.source.sourceRecipeUrl, "cuisine":r});