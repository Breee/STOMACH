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

# Setup the Searchserver (Elasticsearch)

1. start the elasticsearch server located in ``` external/elasticsearch-1.7.5/bin ```.
2. verfy that the search server is running by calling <a href="http://127.0.0.1:9200">127.0.0.1:9200</a> in your browser, 
you will see something similar to the following: 
```
{
  "status" : 200,
  "name" : "Hag",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "1.7.5",
    "build_hash" : "00f95f4ffca6de89d68b7ccaf80d148f1f70e4d4",
    "build_timestamp" : "2016-02-02T09:55:30Z",
    "build_snapshot" : false,
    "lucene_version" : "4.10.4"
  },
  "tagline" : "You Know, for Search"
}
``` 
3. Build the index by calling ```manage.py rebuild_index ```
4. the search should now be working
