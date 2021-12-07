from flask import Flask, abort, url_for 
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Napier"


@app.route('/force404')
def force404():
    abort(404)

@app.route('/force401')
def force401():
    abort(401)

@app.errorhandler(401)
def page_not_found(error):
    return "This page is now located <a href='http://webtech-49.napier.ac.uk:5000'> here </a>"

@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find the page you requested.",404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

