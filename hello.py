from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    
    return"""
            <html>
            <head> 
            <link rel="stylesheet" type="text/css" href="http://webtech-49.napier.ac.uk/style.css">
            </head>
            <body>
            <h1>Look at this cute dog! </h1>
            <img src="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=1.00xw:0.669xh;0,0.190xh&resize=1200:*" width="200" height="100">
            </body>
            </html>
            """
        
   


