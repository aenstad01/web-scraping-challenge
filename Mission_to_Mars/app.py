from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
## note: some of this "chocolate cake recipe" was taken from the Craigslist example from class, so there are still some references to "listings"

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = scrape_mars.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)
    # print(listings)

if __name__ == "__main__":
    app.run(debug=True)
