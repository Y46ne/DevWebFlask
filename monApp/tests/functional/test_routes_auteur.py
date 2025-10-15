from monApp.models import Auteur
from monApp import db
from monApp.tests.functional.test_routes_auteur import login


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
    # Créer un auteur dans la base de données
    with testapp.app_context():
        auteur = Auteur(Nom="Ancien Nom")
        db.session.add(auteur)
        db.session.commit()
        idA = auteur.idA
        # simulation connexion user et soumission du formulaire
        response=login(client, "CDAL", "AIGRE", "/auteur/save/") 
        response = client.post("/auteur/save/", 
        data={"idA": idA,"Nom": "Alexandre Dumas"}, 
        follow_redirects=True)
        # Vérifier que la redirection a eu lieu vers /auteurs/<idA>/view/ et que le contenu 
        # est correct
        assert response.status_code == 200
        assert f"/auteurs/{idA}/view/" in response.request.path
        assert b"Alexandre Dumas" in response.data # contenu de la page vue 
        # Vérifier que la base a été mise à jour
        with testapp.app_context():
            auteur = Auteur.query.get(idA)
            assert auteur.Nom == "Alexandre Dumas"


def test_auteur_insert_success(client, testapp):
    # Créer un auteur dans la base de données
    with testapp.app_context():
        auteur = Auteur(Nom="Ancien Nom")
        db.session.add(auteur)
        db.session.commit()
        idA = auteur.idA
        # simulation connexion user et soumission du formulaire
        response=login(client, "CDAL", "AIGRE", "/auteur/save/") 
        response = client.post("/auteur/save/", 
        data={"idA": idA,"Nom": "Alexandre Dumas"}, 
        follow_redirects=True)
        # Vérifier que la redirection a eu lieu vers /auteurs/<idA>/view/ et que le contenu 
        # est correct
        assert response.status_code == 200
        assert f"/auteurs/{idA}/view/" in response.request.path
        assert b"Alexandre Dumas" in response.data # contenu de la page vue 
        # Vérifier que la base a été mise à jour
        with testapp.app_context():
            auteur = Auteur.query.get(idA)
            assert auteur.Nom == "Alexandre Dumas"

def test_auteur_erase_success(client, testapp):
    # Créer un auteur dans la base de données
    with testapp.app_context():
        auteur = Auteur(Nom="Ancien Nom")
        db.session.add(auteur)
        db.session.commit()
        idA = auteur.idA
        # simulation connexion user et soumission du formulaire
        response=login(client, "CDAL", "AIGRE", "/auteur/save/") 
        response = client.post("/auteur/save/", 
        data={"idA": idA,"Nom": "Alexandre Dumas"}, 
        follow_redirects=True)
        # Vérifier que la redirection a eu lieu vers /auteurs/<idA>/view/ et que le contenu 
        # est correct
        assert response.status_code == 200
        assert f"/auteurs/{idA}/view/" in response.request.path
        assert b"Alexandre Dumas" in response.data # contenu de la page vue 
        # Vérifier que la base a été mise à jour
        with testapp.app_context():
            auteur = Auteur.query.get(idA)
            assert auteur.Nom == "Alexandre Dumas"