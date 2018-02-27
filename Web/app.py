import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, render_template
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.space_stuff
db.dropDatabase()
db = client.space_stuff
collection = db.mars

db.collection.insert_one(thedict)

backdict = db.items.find()

@app.route("/")
def index():

    thedict = scrape()

    return render_template("index.html", 
        output=thedict,
        article_title=thedict['article_title'],
        article_summary=thedict['article_summary'],
        feature_image_url=thedict['feature_image_url'],
        tweet=thedict['tweet'],
        table_html=thedict['table_html'],
        t1=thedict['hemisphere_list'][0]['title'],
        u1=thedict['hemisphere_list'][0]['img_url'],
        t2=thedict['hemisphere_list'][1]['title'],
        u2=thedict['hemisphere_list'][1]['img_url'],
        t3=thedict['hemisphere_list'][2]['title'],
        u3=thedict['hemisphere_list'][2]['img_url'],
        t4=thedict['hemisphere_list'][3]['title'],
        u4=thedict['hemisphere_list'][3]['img_url']
        )

if __name__=="__main__":
    app.run(debug=True)




