from monApp import *
from monApp.models import Livre


def test_livre_liste(client): #client est la fixture définie dans conftest.py
    response = client.get('/livres/')
    assert response.status_code == 200
    assert b'Livre Test' in response.data

def test_livre_update_before_login(client):
    response = client.get('/livres/1/update', follow_redirects=True)
    assert b"Login" in response.data # vérifier redirection vers page Login