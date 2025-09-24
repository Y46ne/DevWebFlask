from .app import app, db
from config import *
from flask import render_template, request
from monApp.models import Auteur, Livre
from monApp.forms import FormAuteur
from flask import url_for, redirect


@app.route('/')

@app.route('/index/')

def index():
    #Si on a pas de paramètre
    if len(request.args) == 0:
        return render_template("index.html",title = "R3.01 Dev Web avec Flask", name = "DefaultName")
    else:
        param_name = request.args.get('name')
        return render_template("index.html",title = "R3.01 Dev Web avec Flask", name = param_name)


@app.route('/about/')

def about():
    return render_template("about.html",title = "R3.01 Dev Web avec Flask, à propos")

@app.route('/infos/')

def info():
    return INFO

@app.route('/credit/')

def credit():
    return CREDIT

@app.route('/contact')

def contact():
    return render_template("contact.html",title = "R3.01 Dev Web avec Flask, contact")

@app.route('/auteurs/')
def getAuteurs():
    lesAuteurs = Auteur.query.all()
    return render_template('auteurs_list.html', title = "R3.01 Dev Web avec Flask", auteurs = lesAuteurs)

@app.route('/livres/')
def getLivres():
    lesLivres = Livre.query.all()
    return render_template('livre_list.html', title = "R3.01 Dev Web avec Flask", livres = lesLivres)

@app.route('/auteurs/<idA>/update')
def updateAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA, Nom = unAuteur.Nom)
    return render_template("auteur_update.html",selectedAuteur=unAuteur,updateForm=unForm)


@app.route('/auteur/save/', methods = ("POST",))
def saveAuteur():
    updatedAuteur = None
    unForm = FormAuteur()
    #recherche de l'auteur à modifier
    idA = int(unForm.idA.data)
    updateAuteur = Auteur.query.get(idA)
    #si les données saisies sont valides pour la mise à jour
    if unForm.validate_on_submit():
        updatedAuteur.Nom = unForm.Nom.data
        db.sessions.commit()
        return redirect(url_for('viewAuteur',idA=updatedAuteur.idA))

    return render_template("auteur_update.html", selectedAuteur=updatedAuteur, viewForm=unForm)

@app.route('/auteurs/<idA</view/')
def viewAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA,Nom=unAuteur.Nom)
    return render_template("auteur_view.html",selectedAuteur=unAuteur, viewForm=unForm)

if __name__ == '__main__':
    app.run()