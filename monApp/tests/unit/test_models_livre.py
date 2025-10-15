from monApp.models import *
def test_livre_init(): 
    livre = Livre(Prix = 9, Titre = "Livre Test", Url = "https://youtube.com", Img = None, auteur_id = 1000)  

    assert livre.Titre == "Livre Test"
    assert livre.Prix == 9
    assert livre.Url == "https://youtube.com"
    
def test_livre_repr(testapp): #testapp est la fixture définie dans conftest.py
    with testapp.app_context():
        livre=Livre.query.get(1)
        assert repr(livre) == "<Livre (1) Livre Test>"