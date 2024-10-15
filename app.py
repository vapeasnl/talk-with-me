from random import sample
from tempfile import mkdtemp
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from better_profanity import profanity  # Import the profanity module
from sqlalchemy.orm import joinedload
from db import db, init_app
from models import Story, Comment, User, UserAction
from functions import get_coms_count, get_pages_count, filter_bad_words
import pagination

# Initialize the Flask application
app = Flask(__name__)

# Profanity filter initialization
profanity.load_censor_words()

# Session configuration
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure the database with the Flask app
init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page if user is not authenticated

# Constant number of stories per page
PER_PAGE = 10

# Load user from user ID (for Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Login to the website
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()  # Clear the current session to avoid conflicts

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate fields
        if not email or not password:
            return render_template("login.html", error="Email and password are required")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):  # Use 'password' instead of 'hash'
            return render_template("login.html", error="Invalid email or password")

        session["user_id"] = user.id  # Store the user's ID in the session
        session["user_profile_picture_url"] = user.profile_picture_url  # Add avatar to the session
        return redirect("/")  # Redirect to the home page

    return render_template("login.html", error=None)
    

# Create necessary tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Submit a new story
@app.route("/submit_story", methods=["POST"])
@login_required  # Ensure the user is logged in
def submit_story():
    content = request.form.get("content")
    filtered_content = filter_bad_words(content)
    
    if filtered_content:
        new_story = Story(content=filtered_content, user_id=current_user.id)
        db.session.add(new_story)
        db.session.commit()
        flash("Your story has been successfully submitted!", "success")
    else:
        flash("The story contains inappropriate words.", "danger")
    
    return redirect(url_for("new"))

# Main page of the site
@app.route("/", defaults={'page': 1})
@app.route('/page/<int:page>')
def home_redirect(page):
    return redirect(url_for('about'))

# New stories page
@app.route("/new", defaults={'page': 1})
@app.route('/new/page/<int:page>')
def new(page):
    if page <= 0:
        return render_template("404.html")

    row = PER_PAGE * (page - 1)
    stories_count = Story.query.count()
    stories = Story.query.order_by(Story.id.desc()).offset(row).limit(PER_PAGE).all()

    if not stories and page != 1:
        return render_template("404.html")

    for story in stories:
        get_coms_count(story)

    pag = pagination.Pagination(page, PER_PAGE, stories_count)
    pages_count = get_pages_count(stories_count)

    user = current_user if current_user.is_authenticated else None

    return render_template("new.html", pagination=pag, stories=stories, pages_count=pages_count, current_page=page, from_where="new", user=user)


# Add a new story
@app.route("/add", methods=["GET", "POST"])
def add():
    user_id = session.get("user_id")

    if request.method == "POST":
        email = request.form.get("email")
        story_text = request.form.get("story")  # Get the story text
        title = request.form.get("title")  # Get the story title

        # Validate input data
        if user_id is None:  # If user is not logged in
            if not email:
                return render_template("add.html", error="Please provide your email.", story=story_text, user_id=user_id)

            user = User.query.filter_by(email=email).first()
            if not user:
                return render_template("add.html", error="This email is not registered.", story=story_text, user_id=user_id)

        if not story_text:
            return render_template("add.html", error="Please provide the text of your story.", email=email, user_id=user_id)

        if not title:
            return render_template("add.html", error="Please provide a title for your story.", email=email, story=story_text, user_id=user_id)

        new_story = Story(title=title, content=story_text, user_id=user_id)  # Use 'content' instead of 'text'
        db.session.add(new_story)

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error adding story: {e}")  # Print error for debugging

    return render_template("add.html", error=None, user_id=user_id)

# View a story with comments

# View a story with comments

@app.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            user_id = session.get("user_id")
            if user_id:
                new_comment = Comment(text=message, story_id=id, user_id=user_id)
                db.session.add(new_comment)
                db.session.commit()
                flash("Your comment has been added!", "success")
            else:
                flash("You must be logged in to comment.", "error")
        return redirect(f"/post/{id}")

    story = Story.query.options(db.joinedload(Story.author)).get_or_404(id)
    comments = Comment.query.filter_by(story_id=id).all()

    user_id = session.get("user_id")
    username = User.query.get(user_id).username if user_id else None
    com_count = len(comments)

    story_data = {
        "id": story.id,
        "title": story.title,
        "content": story.content,
        "author": {
            "id": story.author.id,
            "username": story.author.username,
            "profile_picture_url": story.author.profile_picture_url  # Add profile picture URL
        },
        "datetime": story.datetime,
        "likes": story.likes,
        "dislikes": story.dislikes,
    }

    return render_template('post.html', story=story_data, comments=comments, username=username, com_count=com_count)

# Like a story
@app.route("/like/<int:post_id>/<from_where>", methods=['POST'])
def like(post_id, from_where):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(success=False, message="User not logged in"), 403

    story = Story.query.filter_by(id=post_id).first()
    if not story:
        return jsonify(success=False, message="Story not found"), 404

    action = UserAction.query.filter_by(user_id=user_id, post_id=post_id).first()

    if action:
        if action.liked:
            return jsonify(success=False, message="You have already liked this post")
        elif action.disliked:
            action.liked = True
            action.disliked = False
            story.likes += 1
            story.dislikes -= 1 if story.dislikes > 0 else 0
    else:
        new_action = UserAction(user_id=user_id, post_id=post_id, liked=True)
        db.session.add(new_action)
        story.likes += 1

    db.session.commit()
    return jsonify(success=True, likes=story.likes, dislikes=story.dislikes)

# Dislike a story
@app.route("/dislike/<int:post_id>/<from_where>", methods=['POST'])
def dislike(post_id, from_where):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(success=False, message="User not logged in"), 403

    story = Story.query.filter_by(id=post_id).first()
    if not story:
        return jsonify(success=False, message="Story not found"), 404

    action = UserAction.query.filter_by(user_id=user_id, post_id=post_id).first()

    if action:
        if action.disliked:
            return jsonify(success=False, message="You have already disliked this post")
        elif action.liked:
            action.liked = False
            action.disliked = True
            story.likes -= 1 if story.likes > 0 else 0
            story.dislikes += 1
    else:
        new_action = UserAction(user_id=user_id, post_id=post_id, disliked=True)
        db.session.add(new_action)
        story.dislikes += 1

    db.session.commit()
    return jsonify(success=True, likes=story.likes, dislikes=story.dislikes)

# Like a comment
@app.route("/com_like/<int:com_id>", methods=['POST'])
def com_like(com_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(success=False, message="User not logged in"), 403

    comment = Comment.query.filter_by(id=com_id).first()
    if not comment:
        return jsonify(success=False, message="Comment not found"), 404

    action = UserAction.query.filter_by(user_id=user_id, comment_id=com_id).first()

    if action:
        if action.liked:
            return jsonify(success=False, message="You have already liked this comment")
        elif action.disliked:
            action.liked = True
            action.disliked = False
            comment.likes += 1
            comment.dislikes -= 1 if comment.dislikes > 0 else 0
    else:
        new_action = UserAction(user_id=user_id, comment_id=com_id, liked=True)
        db.session.add(new_action)
        comment.likes += 1

    db.session.commit()
    return jsonify(success=True, likes=comment.likes, dislikes=comment.dislikes)

# Dislike a comment
@app.route("/com_dislike/<int:com_id>", methods=['POST'])
def com_dislike(com_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(success=False, message="User not logged in"), 403

    comment = Comment.query.filter_by(id=com_id).first()
    if not comment:
        return jsonify(success=False, message="Comment not found"), 404

    if comment.dislikes is None:
        comment.dislikes = 0

    action = UserAction.query.filter_by(user_id=user_id, comment_id=com_id).first()

    if action:
        if action.disliked:
            return jsonify(success=False, message="You have already disliked this comment")
        elif action.liked:
            action.liked = False
            action.disliked = True
            comment.likes -= 1 if comment.likes > 0 else 0
            comment.dislikes += 1
    else:
        new_action = UserAction(user_id=user_id, comment_id=com_id, disliked=True)
        db.session.add(new_action)
        comment.dislikes += 1

    db.session.commit()
    return jsonify(success=True, likes=comment.likes, dislikes=comment.dislikes)

# Top stories page
@app.route("/top", defaults={'page': 1})
@app.route('/top/page/<int:page>')
def top(page):
    if page <= 0:
        return render_template("404.html")

    row = PER_PAGE * (page - 1)
    stories_count = Story.query.count()
    stories = Story.query.order_by(Story.likes.desc()).offset(row).limit(PER_PAGE).all()

    if not stories and page != 1:
        return render_template("404.html")

    for story in stories:
        get_coms_count(story)

    pag = pagination.Pagination(page, PER_PAGE, stories_count)
    pages_count = get_pages_count(stories_count)

    return render_template("new.html", pagination=pag, stories=stories, pages_count=pages_count, current_page=page, from_where="top")

# Random stories page
@app.route("/random")
def random():
    count = Story.query.count()
    rep = min(count, 10)
    random_numbers = sample(range(1, count + 1), rep)
    stories = [Story.query.filter_by(id=num).first() for num in random_numbers]

    for story in stories:
        get_coms_count(story)

    return render_template("new.html", stories=stories, from_where="random")

# Logout route
@app.route("/logout")
def logout():
    session.clear()  # Clear the session
    return redirect("/")  # Redirect to the home page

# Register route
# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        avatar = request.form.get("avatar")  # Get selected avatar

        if not email:
            return render_template("register.html", error=1, username=username, text="Please provide email")

        if not username:
            return render_template("register.html", error=2, email=email, text="Please provide username")

        if not password:
            return render_template("register.html", error=3, email=email, username=username, text="Please provide password")

        if password != confirmation:
            return render_template("register.html", error=4, username=username, email=email, text="Passwords don't match")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error=2, email=email, text="Username taken")

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error=1, username=username, text="There's already an account with this email")

        user = User(username=username, email=email, password=generate_password_hash(password), profile_picture_url=avatar)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["user_profile_picture_url"] = user.profile_picture_url  # Add avatar URL to session
        return redirect("/")

    return render_template("register.html", error=None)

# Search for a story with particular words
@app.route("/search", methods=["GET"])
def search():
    subject = request.args.get("subject")

    if not subject:
        return render_template("search_failure.html", text="Empty search query")

    stories = Story.query.filter(Story.text.ilike(f'%{subject}%')).order_by(Story.id.desc()).all()

    if not stories:
        return render_template("search_failure.html", text="There were no results matching the query")

    for story in stories:
        get_coms_count(story)

    return render_template("new.html", stories=stories, pages_count=1, from_where=f"search?subject={subject}")

# About page
@app.route("/about")
def about():
    stories_count = Story.query.count()
    users_count = User.query.count()
    comments_count = Comment.query.count()

    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    return render_template("about.html", stories_count=stories_count, users_count=users_count, comments_count=comments_count, user=user)

# Other routes
@app.route('/stress')
def stress():
    return render_template('stress.html')

@app.route('/importance')
def importance():
    return render_template('importance.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/professional_help')
def professional_help():
    return render_template('professional_help.html')


# Reset password
@app.route("/resetpass", methods=["POST"])
def reset_password():
    email = request.form.get("email")
    new_password = request.form.get("new_password")

    app.logger.debug(f"Reset password attempt for email: {email}")

    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(new_password)  # Ensure field name is 'password'
        db.session.commit()
        flash("Password reset successfully!", "success")
        app.logger.debug(f"Password for {email} reset successfully.")
    else:
        flash("Email not found.", "danger")
        app.logger.debug(f"Email {email} not found.")

    return redirect(url_for("login"))


@app.route("/delete_post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    app.logger.debug(f"Session before deleting post: {session}")
    post = Story.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)  # Forbidden
    comments = Comment.query.filter_by(story_id=post_id).all()
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    app.logger.debug(f"Session after deleting post: {session}")
    flash("Post and associated comments have been deleted.", "success")
    return redirect(url_for("new"))

@app.route("/edit_post/<int:post_id>", methods=["POST"])
@login_required
def edit_post(post_id):
    app.logger.debug(f"Session before editing post: {session}")
    post = Story.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)  # Forbidden
    post.title = request.form.get("title")
    post.text = request.form.get("content")
    db.session.commit()
    app.logger.debug(f"Session after editing post: {session}")
    flash("Post has been updated.", "success")
    return redirect(url_for("post", id=post_id))


# Route to delete a comment
@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)  # Forbidden
    db.session.delete(comment)
    db.session.commit()
    flash("Comment has been deleted.", "success")
    return redirect(url_for("post", id=comment.story_id))


# Route to edit a comment
@app.route("/edit_comment/<int:comment_id>", methods=["POST"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)  # Forbidden
    comment.text = request.form.get("content")
    db.session.commit()
    flash("Comment has been updated.", "success")
    return redirect(url_for("post", id=comment.story_id))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify(authenticated=True)
    else:
        return jsonify(authenticated=False)

# Run the application
if __name__ == '__main__':
    app.run()
