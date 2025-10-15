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
    # simulation connexion user et soumission du formulaire
    response=login(client, "Yasko", "legarsdu41", "/auteur/insert/") 
    response = client.post("/auteur/insert/", 
        data={"Nom": "Jules Verne"}, 
        follow_redirects=True)
    # Vérifier que la redirection a eu lieu et que le contenu est correct
    assert response.status_code == 200
    assert b"Jules Verne" in response.data # contenu de la page vue
    # Vérifier que la base a été mise à jour
    with testapp.app_context():
        # Le nouvel auteur devrait avoir l'id 2 (le premier est créé dans conftest)
        auteur = Auteur.query.get(2)
        assert auteur is not None
        assert auteur.Nom == "Jules Verne"

def test_auteur_erase_success(client, testapp):
    # Créer un auteur dans la base de données
    with testapp.app_context():
        idA = 1 # L'auteur "Victor Hugo" créé dans conftest
        # simulation connexion user et soumission du formulaire pour la suppression
        response=login(client, "Yasko", "legarsdu41", f"/auteurs/{idA}/delete/") 
        response = client.post("/auteur/erase/", data={"idA": idA}, follow_redirects=True)
        # Vérifier que la redirection a eu lieu vers la liste des auteurs
        assert response.status_code == 200
        assert request.path == "/auteurs/"
        # Vérifier que l'auteur n'est plus dans la base
        with testapp.app_context():
            auteur = Auteur.query.get(idA)
            assert auteur is None