from .app import app, db
from config import *
from flask import render_template, request
from monApp.models import Auteur, Livre, User
from monApp.forms import *
from flask import url_for, redirect
from flask_login import *
from hashlib import sha256


@app.route('/')
@app.route('/index/')
def index():
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

@app.route('/livres/<int:idL>/update')
@login_required
def updateLivre(idL):
    unLivre = Livre.query.get_or_404(idL)
    unForm = FormLivre(obj=unLivre)
    return render_template("livre_update.html",selectedLivre=unLivre,updateForm=unForm)

@app.route('/livre/save/', methods = ("POST",))
@login_required
def saveLivre():
    unForm = FormLivre()
    
    # BUG FIX: Use the actual ID from the form, not a hardcoded value 🐞
    idL = int(unForm.idL.data)
    updatedLivre = Livre.query.get_or_404(idL)
    
    if unForm.validate_on_submit():
        updatedLivre.Prix = unForm.Prix.data
        db.session.commit()
        return redirect(url_for('viewLivre',idL=updatedLivre.idL))

    # If form is invalid, re-render the update page with the same form
    return render_template("livre_update.html", selectedLivre=updatedLivre, updateForm=unForm)

@app.route('/livres/<idL>/view/') # Good practice to specify type
def viewLivre(idL):
    unLivre = Livre.query.get_or_404(idL)
    unForm = FormLivre(obj=unLivre) # Pre-populate form
    
    
    return render_template("livre_view.html",selectedLivre=unLivre, viewForm=unForm)

# ... (Rest of your code for Auteurs, login, logout, etc.)
# ... (It can stay as it was)


@app.route('/auteurs/<idA>/update')
@login_required
def updateAuteur(idA):
    unAuteur = Auteur.query.get_or_404(idA)
    unForm = FormAuteur(obj=unAuteur)
    return render_template("auteur_update.html",selectedAuteur=unAuteur,updateForm=unForm)


@app.route('/auteur/save/', methods = ("POST",))
@login_required
def saveAuteur():
    unForm = FormAuteur()
    idA = int(unForm.idA.data)
    updatedAuteur = Auteur.query.get_or_404(idA)

    if unForm.validate_on_submit():
        updatedAuteur.Nom = unForm.Nom.data
        db.session.commit()
        return redirect(url_for('viewAuteur',idA=updatedAuteur.idA))

    return render_template("auteur_update.html", selectedAuteur=updatedAuteur, updateForm=unForm)

@app.route('/auteurs/<idA>/view/')
def viewAuteur(idA):
    unAuteur = Auteur.query.get_or_404(idA)
    unForm = FormAuteur(obj=unAuteur)
    return render_template("auteur_view.html",selectedAuteur=unAuteur, viewForm=unForm)

@app.route('/auteur/create') # Changed route to be more descriptive
@login_required
def createAuteur():
    unForm = FormAuteur()
    return render_template("auteur_create.html", createForm=unForm)

@app.route('/auteur/insert/', methods=("POST",))
@login_required
def insertAuteur():
    unForm = FormAuteur()
    if unForm.validate_on_submit(): 
        existingAuteur = Auteur.query.filter_by(Nom=unForm.Nom.data).first()
        if existingAuteur:
            Warning("l'auteur existe déjà")
            return render_template("auteur_create.html", createForm=unForm)
        insertedAuteur = Auteur(Nom=unForm.Nom.data)
        db.session.add(insertedAuteur)
        db.session.commit()
        return redirect(url_for('viewAuteur', idA=insertedAuteur.idA))
    return render_template("auteur_create.html", createForm=unForm)



@app.route('/auteurs/<int:idA>/delete/')
@login_required
def deleteAuteur(idA):
    unAuteur = Auteur.query.get_or_404(idA)
    unForm = FormAuteur(obj=unAuteur)
    return render_template("auteur_delete.html",selectedAuteur=unAuteur, deleteForm=unForm)


@app.route ('/auteur/erase/', methods =("POST" ,))
@login_required
def eraseAuteur():
    unForm = FormAuteur()
    idA = int(unForm.idA.data)
    deletedAuteur = Auteur.query.get_or_404(idA)
    db.session.delete(deletedAuteur)
    db.session.commit()
    return redirect(url_for('getAuteurs'))

@app.route ("/login/", methods =("GET","POST" ,))
def login():
    unForm = LoginForm()
    if unForm.validate_on_submit():
        unUser = unForm.get_authenticated_user()
        if unUser:
            login_user(unUser)
            next_page = request.args.get('next') or url_for("index",name=unUser.Login)
            return redirect(next_page)
    return render_template ("login.html",form=unForm)

@app.route ("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signin/", methods=["GET", "POST"])
def signin():
    unForm = SignInForm()
    if unForm.validate_on_submit():
        m = sha256()
        m.update(unForm.Password.data.encode())
        passwd = m.hexdigest()
        insertedUser = User(Login=unForm.Login.data,Password=passwd)
        db.session.add(insertedUser)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("signin.html",form=unForm)

if __name__ == '__main__':
    app.run(debug=True)