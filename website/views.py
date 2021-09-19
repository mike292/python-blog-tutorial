from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = (
        Post.query.all()
    )  # Take all the post in the database and returns a set of objects
    print("Query Post in home:", posts)
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")
        print("Posted text:", text)
        if not text:
            flash("Please write a something.", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Successfully post somethings", category="success")
            return redirect(url_for("views.home"))
        pass
    return render_template("create_post.html", user=current_user)


@views.route("/posts/<id>")
@login_required
def posts(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        flash("No user with that username", category="error")
        return redirect(url_for("views.home"))

    # posts = Post.query.filter_by(author=id).all()
    posts = user.posts
    return render_template(
        "posts.html", user=current_user, posts=posts, username=user.username
    )


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    # remove later
    print("Post to be deleted:", post, post.id, post.author)
    print("Current user id", current_user.id)

    if not post:
        flash("Post does not exist", category="error")
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", category="success")

    return redirect(url_for("views.home"))


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")
    print("The post id is:", post_id)
    print("The Comment is:", text)

    if not text:
        flash("Comment is empty", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        print("Post in create comment:", post)
        if not post:
            flash("Post does not exist", category="error")
        else:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            print("Success comment")

    return redirect(url_for("views.home"))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash("Comment does not exist", category="error")
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("You do not have permission to delete this comment", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("views.home"))


@views.route("/like-post/<post_id>", methods=["POST"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({"error": "post does not exist."}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify(
        {
            "likes": len(post.likes),
            "liked": current_user.id in map(lambda x: x.author, post.likes),
        }
    )
