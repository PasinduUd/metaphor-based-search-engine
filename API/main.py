from flask import Flask, render_template, request

import es_client

es = es_client.ESClient()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def root():
    songs = []
    if request.method == "POST":
        if "logical_combination_search" in request.form:
            req_body = request.form.to_dict(flat=True)
            songs = es.get_logical_combinations(req_body)
            print("# Songs : ", len(songs))
        return render_template("advanced_search_engine.html", songs=songs)
    return render_template("advanced_search_engine.html", songs=[])



# @app.route("/", methods=["GET"])
# def root():
#     return render_template("advanced_search_engine.html", songs=[])

# @app.route("/logical-combination",  methods=["POST"])
# def logical_combination():
#     print(request.form)
#     # if request.method == 'POST':
#         # if 'form_1' in request.form:
#         #     if request.form['nm']:
#         #         search = request.form['nm']
#         #         global_search = search
#         #         print(global_search)
#     print(es.get_all_songs())
#     return render_template("advanced_search_engine.html", songs=es.get_all_songs())

if __name__ == "__main__":
    app.run(debug=True)