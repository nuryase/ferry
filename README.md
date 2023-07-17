# Ferry

## Usage
Clone the repository.

``````
$ git clone git@github.com:yasenne/ferry.git
``````

Move into ```ferry``` directory and create a virtual environment.

``````
$ cd ferry
$ python3 -m venv .venv
$ source .venv/bin/activate
``````

Initialize the database.

``````
$ flask --app ferry init-db
``````

Run the app.

``````
$ flask --app ferry run
``````

When making a log, ```title``` refers to the post title.
```artist``` refers to the name of the artist you want to recieve recommendations for. 
```genres``` refers to the genres you want the recommendations to focus on.
```track``` refers to the name of the track you want to recieve recommendations for.

The user can have a total of 5 inputs from artist, genres, and track combined.

e.g. ```artist: Deafheaven | genres: blackgaze, shoegaze | track: Dream House```

## Misc
List of genres: [spotify-genres.md](https://gist.github.com/andytlr/4104c667a62d8145aa3a)
