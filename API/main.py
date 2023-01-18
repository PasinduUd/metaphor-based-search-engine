from flask import Flask, render_template, request

import es_connector
import models

es = es_connector.ESConnector()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        if "logical_combination_search" in request.form:
            body = request.form.to_dict(flat=True)
            print(body["operation"])
        return render_template("advanced_search_engine.html", songs=es.get_all_songs())
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