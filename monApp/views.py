from .app import app
from config import *

@app.route('/')

def index():
    return "Hello, World!"

@app.route('/about/')

def about():
    return ABOUT

@app.route('/infos/')

def info():
    return INFO

@app.route('/credit/')

def info():
    return CREDIT

if __name__ == '__main__':
    app.run()