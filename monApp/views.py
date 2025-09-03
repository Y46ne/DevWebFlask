from flask import Flask

app = Flask(__name__)

@app.route('/')

def index( ) :
    return "Skibidi bop yes yes yes"

if __name__== "__main__" :
    app.run( )