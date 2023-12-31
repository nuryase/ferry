from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from ferry.auth import login_required
from ferry.db import get_db
from ferry.client import *

bp = Blueprint("logs", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, artist, genres, track, recommendations, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()

    return render_template("logs/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        artist = request.form["artist"]
        genres = request.form["genres"]
        track = request.form["track"]

        client = Client()
        data = client.recommendations_search(artist, genres, track)
        recommendations = client.get_recommendations(data)

        # print(recommendations)

        error = None

        if not title:
            error = "Title is required."
        if not artist:
            error = "Artist(s) are required."

        if not genres:
            error = "Genre(s) are required."

        if not track:
            error = "Track(s) are required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, artist, genres, track, recommendations, author_id)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (title, artist, genres, track, recommendations, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("logs.index"))

    return render_template("logs/create.html")


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, artist, genres, track, recommendations, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        # artist = request.form["artist"]
        # genres = request.form["genres"]
        # track = request.form["track"]
        error = None

        # if not artist:
        if not title:
            error = "Title is required."

        # if not genres:
        # error = "Genre(s) are required."

        # if not track:
        # error = "Track is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?" " WHERE id = ?",
                (title, id),
            )
            db.commit()
            return redirect(url_for("logs.index"))

    return render_template("logs/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("logs.index"))
