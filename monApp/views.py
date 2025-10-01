from .app import app, db
from config import *
from flask import render_template, request
from monApp.models import Auteur, Livre
from monApp.forms import FormAuteur, FormLivre
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

@app.route('/livres/<idL>/update')
def updateLivre(idL):
    unLivre = Livre.query.get(idL)
    unForm = FormLivre(idA = unLivre.idL, Prix = unLivre.Prix)
    return render_template("livre_update.html",selectedLivre=unLivre,updateForm=unForm)

@app.route('/livre/save/', methods = ("POST",))
def saveLivre():
    updatedLivre = None
    unForm = FormLivre()
    #recherche du livre à modifier
    idL = int(unForm.idL.data)
    updatedLivre = Livre.query.get(idL)
    #si les données saisies sont valides pour la mise à jour
    if unForm.validate_on_submit():
        updatedLivre.Nom = unForm.Nom.data
        db.session.commit()
        return redirect(url_for('viewLivre',idL=updatedLivre.idL))

    return render_template("livre_update.html", selectedLivre=updatedLivre, viewForm=unForm)

@app.route('/livres/<idL>/view/')
def viewLivre(idL):
    unLivre = Livre.query.get(idL)
    unForm = FormLivre(idA=unLivre.idL,Nom=unLivre.Prix)
    return render_template("livre_view.html",selectedLivre=unLivre, viewForm=unForm)



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
    updatedAuteur = Auteur.query.get(idA)
    #si les données saisies sont valides pour la mise à jour
    if unForm.validate_on_submit():
        updatedAuteur.Nom = unForm.Nom.data
        db.session.commit()
        return redirect(url_for('viewAuteur',idA=updatedAuteur.idA))

    return render_template("auteur_update.html", selectedAuteur=updatedAuteur, viewForm=unForm)

@app.route('/auteurs/<idA>/view/')
def viewAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA,Nom=unAuteur.Nom)
    return render_template("auteur_view.html",selectedAuteur=unAuteur, viewForm=unForm)

@app.route('/auteur/')
def createAuteur():
    unForm = FormAuteur()
    return render_template("auteur_create.html", createForm=unForm)

@app.route ('/auteur/insert/', methods =("POST" ,))
def insertAuteur():
    insertedAuteur = None
    unForm = FormAuteur()
    if unForm.validate_on_submit(): 
        insertedAuteur = Auteur(Nom=unForm.Nom.data)
        db.session.add(insertedAuteur)
        db.session.commit()
        insertedId = Auteur.query.count()
        return redirect(url_for('viewAuteur', idA=insertedId))
    return render_template("auteur_create.html", createForm=unForm)


@app.route('/auteurs/<idA>/delete/')
def deleteAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA, Nom=unAuteur.Nom)
    return render_template("auteur_delete.html",selectedAuteur=unAuteur, deleteForm=unForm)


@app.route ('/auteur/erase/', methods =("POST" ,))
def eraseAuteur():
    deletedAuteur = None
    unForm = FormAuteur()
    #recherche de l'auteur à supprimer
    idA = int(unForm.idA.data)
    deletedAuteur = Auteur.query.get(idA)
    #suppression
    db.session.delete(deletedAuteur)
    db.session.commit()
    return redirect(url_for('getAuteurs'))



if __name__ == '__main__':
    app.run()