from monApp.models import *

def test_user_init(): 
    user = User(Login = "Yasko", Password = "legarsdu41")
    assert user.Login == "Yasko"
    assert user.Password == "legarsdu41"    