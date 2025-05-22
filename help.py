from flask import Flask, render_template, request
import requests

app = Flask(__name__)

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any"

@app.route("/", methods=["GET"])
def index():
    category = request.args.get("category", "Any")
    params = {
        "format": "json",
        "type": "single"  # Can be 'single' or 'twopart'
    }
    response = requests.get(f"https://v2.jokeapi.dev/joke/{category}", params=params)
    data = response.json()

    if data.get("error"):
        joke = "Oops! Couldn't fetch a joke right now."
    else:
        if data.get("type") == "single":
            joke = data.get("joke")
        else:
            joke = f"{data.get('setup')} ... {data.get('delivery')}"

    return render_template("index.html", joke=joke, category=category)

if __name__ == "__main__":
    app.run(debug=True)