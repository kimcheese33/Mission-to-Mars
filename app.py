###import tools

#use Flask to render a template.
from flask import Flask, render_template
#use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
#to use scraping code, convert jupyter notebook to python
import scraping


#set up flask
app = Flask(__name__)

###use flask_pymongo to set up mongo connection

#tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
#is the URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app"
mongo = PyMongo(app)


#define route for html page
@app.route('/')
def index():
    #uses pymongo to find mars collection
    mars = mongo.db.mars.find_one()
    #tell flask to return an html template using an index.html file, using the mars collection in mongodb
    return render_template('index.html', mars=mars)

#add scraping route
@app.route('/scrape')
def scrape():
    #access DB
    mars = mongo.db.mars
    #scrape using scraping.py
    mars_data = scraping.scrape_all()
    #update DB
    mars.update({}, mars_data, upsert=True)
    return 'Scraping Successful!'

#code to run flask
if __name__ == "__main__":
    app.run()