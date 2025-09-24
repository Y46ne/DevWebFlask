#>>>import random string os
#>>>"".join([random.choice(string.printable)for _in os.urandom(24)])
import os

SECRET_KEY = "2lzUl{$*D6#`8uXqlU."
ABOUT = "Bienvenue sur la page à propos de Flask !"
INFO = "Ceci est une application de démonstration pour Flask faites par le goat Yassine B."
CREDIT = "Developpeur : Belaarous Yassine"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'monApp.db')
BOOTSTRAP_SERVE_LOCAL = True