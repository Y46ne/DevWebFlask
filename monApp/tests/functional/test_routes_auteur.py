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