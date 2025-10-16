from hashlib import sha256
from monApp.models import Auteur
from monApp import db


def test_auteurs_liste(client): #client est la fixture définie dans conftest.py
    response = client.get('/auteurs/')
    assert response.status_code == 200
    assert b'Victor Hugo' in response.data


def login(client, username, password, next_path):
    return client.post(   "/login/", 
        data={"Login": username,"Password": password, "next":next_path} ,
        follow_redirects=True)

def test_auteur_update_before_login(client):
    response = client.get('/auteurs/1/update', follow_redirects=True)
    assert b"Login" in response.data # vérifier redirection vers page Login 

def test_auteur_save_success(client, testapp):
    with testapp.app_context():
        auteur = Auteur(Nom="Ancien Nom de Test")
        db.session.add(auteur)
        db.session.commit()
        idA = auteur.idA
        response=login(client, "CDAL", sha256("AIGRE").hexdigest(), "/auteur/save/") 
        response = client.post("/auteur/save/", 
        data={"idA": idA,"Nom": "Alexandre Dumas"}, 
        follow_redirects=True)

        assert response.status_code == 200
        assert f"/auteurs/{idA}/view/" in response.request.path
        assert b"Alexandre Dumas" in response.data # contenu de la page vue 
        with testapp.app_context():
            auteur = Auteur.query.get(idA)
            assert auteur.Nom == "Alexandre Dumas"

def test_auteur_creation_fails_if_name_exists(client, testapp):
    with testapp.app_context():
        auteur = Auteur(Nom="Victor Hugo")
        db.session.add(auteur)
        db.session.commit()
    login(client, "CDAL", sha256("AIGRE").hexdigest(), "/auteur/create/")
    response = client.post("/auteur/create/",
    data={"Nom": "Victor Hugo"},
    follow_redirects=True)

    assert response.status_code == 200
    assert b"Le nom de l'auteur existe d\xc3\xa9j\xc3\xa0" in response.data