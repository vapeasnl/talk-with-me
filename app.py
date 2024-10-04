from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint, sample
from db import db, init_app
from models import Story, Comment, User
from functions import get_coms_count, get_pages_count, filter_bad_words  # Assurez-vous que cette fonction est définie
from flask_login import LoginManager, current_user, login_required
import pagination

# Initialiser l'application Flask
app = Flask(__name__)

# Configurer la session pour utiliser le système de fichiers
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialiser db avec l'application Flask
init_app(app)

# Initialiser le LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Rediriger vers la route de connexion si non authentifié

# Nombre constant de stories par page
PER_PAGE = 10

# Chargez l'utilisateur à partir de l'identifiant
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()  # Crée les tables si elles n'existent pas

@app.route("/submit_story", methods=["POST"])
def submit_story():
    content = request.form.get("content")
    filtered_content = filter_bad_words(content)
    
    if filtered_content:
        new_story = Story(content=filtered_content, user_id=current_user.id)
        db.session.add(new_story)
        db.session.commit()
        flash("Votre histoire a été soumise avec succès !", "success")
    else:
        flash("L'histoire contient des mots inappropriés.", "danger")
    
    return redirect(url_for("new"))

@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
@login_required  # Assurez-vous que l'utilisateur est connecté
def profile(user_id):
    user = User.query.get(user_id)
    if request.method == "POST":
        user.username = request.form.get("username")
        user.email = request.form.get("email")
        # Code to handle profile picture upload
        profile_picture = request.files.get("profile_picture")
        if profile_picture:
            # Save profile picture and update URL
            user.profile_picture_url = save_profile_picture(profile_picture)
        db.session.commit()
        flash("Votre profil a été mis à jour avec succès !", "success")
        return redirect(f"/profile/{user_id}")
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)  # Démarrer le serveur

    
# Page principale du site
@app.route("/", defaults={'page': 1})
@app.route('/page/<int:page>')
def home_redirect(page):
    return redirect(url_for('about'))



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

    # Ajoutez la variable `user` ici
    user = current_user if current_user.is_authenticated else None

    return render_template("new.html", pagination=pag, stories=stories, pages_count=pages_count, current_page=page, from_where="new", user=user)

@app.route("/add", methods=["GET", "POST"])
def add():
    try:
        user_id = session["user_id"]
    except KeyError:
        user_id = None

    if request.method == "POST":
        email = request.form.get("email")
        story_text = request.form.get("story")  # Récupérer le texte de l'histoire
        title = request.form.get("title")  # Récupérer le titre de l'histoire

        # Validation des données
        if user_id is None:  # Si l'utilisateur n'est pas connecté
            # Vérifiez si l'email est fourni
            if not email:
                return render_template("add.html", error="Please provide your email.", story=story_text, user_id=user_id)

            # Vérifiez si l'email existe dans la base de données
            user = User.query.filter_by(email=email).first()  # Remplacez 'User' par votre modèle d'utilisateur
            if not user:
                return render_template("add.html", error="This email is not registered.", story=story_text, user_id=user_id)

        # Validation du texte de l'histoire
        if not story_text:
            return render_template("add.html", error="Please provide the text of your story.", email=email, user_id=user_id)

        if not title:  # Assurez-vous que le titre est fourni
            return render_template("add.html", error="Please provide a title for your story.", email=email, story=story_text, user_id=user_id)

        # Créer une nouvelle histoire avec le titre et le texte
        new_story = Story(title=title, text=story_text, user_id=user_id)  # Assurez-vous d'inclure user_id si l'utilisateur est connecté
        db.session.add(new_story)

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()  # Annuler en cas d'erreur
            print(f"Erreur lors de l'ajout de l'histoire: {e}")  # Imprimer l'erreur pour le débogage

    return render_template("add.html", error=None, user_id=user_id)

# Voir une story avec des commentaires
@app.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    message = request.form.get("message")
    
    if request.method == "POST" and message:
        user_id = session["user_id"]
        new_comment = Comment(text=message, story_id=id, user_id=user_id)  # Changer post_id en story_id
        db.session.add(new_comment)
        db.session.commit()
        return redirect("/post/{}".format(id))
    else:
        story = Story.query.get_or_404(id)  # Utiliser get_or_404 pour une meilleure gestion des erreurs
        comments = Comment.query.filter_by(story_id=id).all()  # Changer post_id en story_id

        if session.get("user_id") is None:
            username = None
        else:
            user = User.query.get(session["user_id"])
            username = user.username

        com_count = len(comments)

        return render_template("post.html", story=story, comments=comments, com_count=com_count, username=username, error=None)


@app.route("/like/<int:post_id>/<from_where>", methods=['POST'])
def like(post_id, from_where):
    print(f'Like request for post: {post_id}')  # Ajoutez ceci
    story = Story.query.filter_by(id=post_id).first()
    if story:
        story.likes += 1
        db.session.commit()
    return jsonify(success=True)

@app.route("/dislike/<int:post_id>/<from_where>", methods=['POST'])
def dislike(post_id, from_where):
    print(f'Dislike request for post: {post_id}')  # Ajoutez ceci
    story = Story.query.filter_by(id=post_id).first()
    if story:
        story.likes -= 1
        db.session.commit()
    return jsonify(success=True)
    
@app.route("/com_like/<int:com_id>", methods=['POST'])
def com_like(com_id):
    comment = Comment.query.filter_by(id=com_id).first()
    if comment:
        comment.likes += 1
        db.session.commit()
        print(f"Comment ID: {com_id}, New Likes: {comment.likes}")  # Log pour débogage
        return jsonify(success=True, likes=comment.likes)
    return jsonify(success=False, message="Comment not found"), 404

@app.route("/com_dislike/<int:com_id>", methods=['POST'])
def com_dislike(com_id):
    comment = Comment.query.filter_by(id=com_id).first()
    if comment:
        comment.likes -= 1
        db.session.commit()
        print(f"Comment ID: {com_id}, New Likes: {comment.likes}")  # Log pour débogage
        return jsonify(success=True, likes=comment.likes)
    return jsonify(success=False, message="Comment not found"), 404


# Top section
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


# Random section
@app.route("/random")
def random():
    count = Story.query.count()
    rep = min(count, 10)
    random_numbers = sample(range(1, count + 1), rep)
    stories = [Story.query.filter_by(id=num).first() for num in random_numbers]

    for story in stories:
        get_coms_count(story)

    return render_template("new.html", stories=stories, from_where="random")

# Login to the website
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()  # Efface la session actuelle pour éviter des conflits

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Validation des champs
        if not email or not password:
            return render_template("login.html", error="Email and password are required")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.hash, password):
            return render_template("login.html", error="Invalid email or password")

        session["user_id"] = user.id  # Stocke l'ID de l'utilisateur dans la session
        session["user_profile_picture_url"] = user.profile_picture_url  # Ajoute l'avatar dans la session
        return redirect("/")  # Redirige vers la page d'accueil

    return render_template("login.html", error=None)


# Logout from the website
@app.route("/logout")
def logout():
    session.clear()  # Efface la session
    return redirect("/")  # Redirige vers la page d'accueil


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

        user = User(username=username, email=email, hash=generate_password_hash(password), profile_picture_url=avatar)  # Save avatar choice
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["user_profile_picture_url"] = user.profile_picture_url  # Add avatar URL to session
        return redirect("/")

    return render_template("register.html", error=None)


# Search a story with particular words
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


@app.route("/about")
def about():
    stories_count = Story.query.count()
    users_count = User.query.count()
    comments_count = Comment.query.count()

    # Vérifiez si l'utilisateur est connecté et obtenez l'utilisateur
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    return render_template("about.html", stories_count=stories_count, users_count=users_count, comments_count=comments_count, user=user)
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

