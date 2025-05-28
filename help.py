from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    category = request.args.get("category", "Any")
    params = {
        "format": "json",
        "type": "single"
    }

    try:
        response = requests.get(f"https://v2.jokeapi.dev/joke/{category}", params=params, timeout=5)
        response.raise_for_status()  # Raise error if HTTP status code is 4xx/5xx
        data = response.json()

        if data.get("error"):
            joke = "Oops! Couldn't fetch a joke right now."
        else:
            if data.get("type") == "single":
                joke = data.get("joke")
            else:
                joke = f"{data.get('setup')} ... {data.get('delivery')}"

        return render_template("index.html", joke=joke, category=category)

    except requests.exceptions.RequestException as e:
        return render_template("error.html", error_message=str(e)), 503
    except Exception:
        return render_template("error.html", error_message="An unexpected error occurred."), 500

@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error_message="404 - Page Not Found"), 404

if __name__ == "__main__":
    app.run(debug=True)