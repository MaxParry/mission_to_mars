import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, render_template, jsonify, redirect
import pymongo
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

mongo = PyMongo(app)

# ok, things are working.
# need to html a button to route to /scrape
# need to (maybe) figure out how to run mongod automatically at terminal so site works
# need to write bootstrap site

@app.route("/")
def index():
    try:
        returned_dict = mongo.db.mars.find_one()
    except:
        print('No DB yet')
        return('No DB yet, start the mongo server from shell')

    return render_template("index.html", 
        output=returned_dict,
        article_title=returned_dict['article_title'],
        article_summary=returned_dict['article_summary'],
        feature_image_url=returned_dict['feature_image_url'],
        tweet=returned_dict['tweet'],
        table_html=returned_dict['table_html'],
        t1=returned_dict['hemisphere_list'][0]['title'],
        u1=returned_dict['hemisphere_list'][0]['img_url'],
        t2=returned_dict['hemisphere_list'][1]['title'],
        u2=returned_dict['hemisphere_list'][1]['img_url'],
        t3=returned_dict['hemisphere_list'][2]['title'],
        u3=returned_dict['hemisphere_list'][2]['img_url'],
        t4=returned_dict['hemisphere_list'][3]['title'],
        u4=returned_dict['hemisphere_list'][3]['img_url']
        )

@app.route("/lets_scrape")
def lets_scrape():
    thedict = scrape()
    mars = mongo.db.mars
    mars.update(
        {},
        thedict,
        upsert=True
    )

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)




