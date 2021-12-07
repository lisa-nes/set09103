from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():

    start = """<html><head><link rel='stylesheet' type='text/css' href='"""
    url = url_for('static', filename='style.css')
    end = """'></head><body><h1>Look at this cute dog!</h1><img src="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/
                images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=1.00xw:0.669xh;
                0,0.190xh&resize=1200:*" width="200" height="100">
            </body>
            </html>"""

     return start+url+end, 200

 if __name__ == "__main__":           
     app.run(host='0.0.0.0', debug=True)


