from flask import Flask, render_template, request
import es_client

app = Flask(__name__)
es = es_client.ESClient()

@app.route("/", methods=["GET", "POST"])
def root():
    songs = []
    if request.method == "POST":
        if "advanced_search" in request.form:
            songs = es.advanced_search(request.form.to_dict(flat=True))
        elif "logical_combination_search" in request.form:
            songs = es.get_logical_combinations(request.form.to_dict(flat=True))
        else:
            songs = es.regular_search(request.form.to_dict(flat=True))
        print("# Songs : ", len(songs))
        return render_template("search_engine.html", songs=songs)
    return render_template("search_engine.html", songs=[])

if __name__ == "__main__":
    app.run(debug=True)