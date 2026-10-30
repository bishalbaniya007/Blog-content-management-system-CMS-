from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Post
from app.forms.post_form import PostForm


posts = Blueprint("posts", __name__)

@posts.route("/new", methods=["GET", "POST"])
@login_required
def create():
  form = PostForm()

  if form.validate_on_submit():
    # post is an instance of Post class(Table)
    post = Post(
      title = form.title.data,
      body = form.body.data,
      status = form.status.data,
      author = current_user # current_user return User object
    )

    db.session.add(post)
    db.session.commit()

    flash("Post saved.")
    return redirect(url_for("posts.detail", post_id = post.id))

  return render_template("post_form.html", form=form, heading="New Post")


@posts.route("/detail/<int:post_id>")
@login_required
def detail(post_id):
  post = db.get_or_404(Post, post_id)
  
