import pytest
from monApp import *
from monApp.models import Auteur, Livre, User
@pytest.fixture
def testapp():
    app.config.update({"TESTING":True,"SQLALCHEMY_DATABASE_URI":
    "sqlite:///:memory:","WTF_CSRF_ENABLED": False})
    with app.app_context():
        db.create_all()
        # Ajouter un auteur de test
        auteur = Auteur(Nom="Victor Hugo")
        db.session.add(auteur)
        db.session.commit()

        livre = Livre(Prix = 9, Titre = "Livre Test", Url = "https://youtube.com", Img = None, auteur_id = 1000)  
        db.session.add(livre)
        db.session.commit()

        user = User(Login = "Yasko", Password = "legarsdu41")
        db.session.add(user)
        db.session.commit()
        
    yield app
    # Cleanup après les tests
    with app.app_context():
        db.drop_all()
@pytest.fixture
def client(testapp):
    return testapp.test_client()