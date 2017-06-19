# STOMACH
STOck MAnager and Cooking Helper.

# Was ist STOMACH?
Geplant ist ein Tool um Kochrezepte in einem Profil anzulgegen und ggf. mit anderen zu teilen.
Der Clou ist, man kann die Rezepte "umrechnen" lassen wenn man zb. zu wenige Zutaten hat um das "große" Rezept zu
kochen.

Ausserdem ist ein "Inventar" an Bord, über welches man sich Rezepte generieren lassen kann und eine Übersicht über seine Zutaten hat.

# Installing
So this Tool is written in Django.

Requirements are: Python 3 and Pip.

1. Clone the Repo and cd to the download dir.
2. Install the requirements with:

```pip install -r requirements.txt```

3. Setup the Settings-File:

```cd STOMACH```

then open the ```settings.py``` File with your favorite Editor.
For Productive use set ```DEBUG = False```.

If you want to use your favorite Database change the Settings to your favorite Database, Django should Hanlde the rest.

For more information on Database Setup see the Django Documentation <a href="https://docs.djangoproject.com/en/1.11/ref/settings/">here</a>.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

# Setup the Search (Woosh)

1. Build the index by calling ```manage.py rebuild_index ```
2. the search should now be working
