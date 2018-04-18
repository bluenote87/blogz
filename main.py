from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:alwaysbecoding@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "#mysecretkey"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return "<Blog %r>" % self.title

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(60))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User %r>" % self.username

@app.before_request
def require_login():
    allowed_routes = ['log_on', 'new_account', 'index', 'view_a_post']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route("/blog")
def view_a_post():
    post_id = request.args.get('id')
    if post_id:
        post = Blog.query.filter_by(id=post_id).first()
        author = post.owner
        return render_template('viewpost.html', post=post, author=author.__class__.__name__,
            title = "You are viewing a single post")
            # TODO - fix the author name attribute to show as a string, not an object
    else:
        posts = Blog.query.all()
        return render_template('blog.html', title="My Awesome Dynamic Blog", posts=posts)
    

@app.route('/newpost', methods = ['POST', 'GET'])
def add_a_post():

    title_error = ""
    body_error = ""
    
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        author = User.query.filter_by(username=session['username']).first()
        
        if blog_title == "":
            title_error = "I need something in the title before posting!"
        if len(blog_title) > 120:
            title_error = "That title is too long! Please keep it under 120 characters."
        if blog_body == "":
            body_error = "I need something in the body before posting!"
        if title_error or body_error:
            return render_template('newpost.html', title="My Awesome Dynamic Blog", 
                title_redux = blog_title, body_redux = blog_body, title_error=title_error, body_error=body_error)
        else:
            new_blog = Blog(blog_title, blog_body, author)
            db.session.add(new_blog)
            db.session.commit()
            new_id = new_blog.id
            return redirect('blog?id={0}.html'.format(new_id))
    else:
        return render_template('newpost.html', title="My Awesome Dynamic Blog", 
            title_redux = "", body_redux = "", title_error=title_error, body_error=body_error)

@app.route('/signup', methods = ['POST', 'GET'])
def new_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        un_error = ""
        pw_error = ""
        pv_error = ""

        existing_user = User.query.filter_by(username=username).first()

        if username == "":
            un_error = "That's not a valid username"
        elif len(username) > 120 or len(username) < 3:
            un_error = "That's not a valid username"

        un_ver = re.search(r'\s|\W', username)
        if un_ver:
            un_error = "That's not a valid username"

        if password == "":
            pw_error = "That's not a valid password"
        elif len(password) > 60 or len(password) < 3:
            pw_error = "That's not a valid password"

        if verify == "":
            pv_error = "Passwords don't match"
        elif len(verify) > 60 or len(verify) < 3:
            pv_error = "Passwords don't match"
        elif verify != password:
            pv_error = "Passwords don't match"

        if un_error or pw_error or pv_error:
            return render_template('signup.html', username=username, un_error=un_error, pw_error=pw_error, pv_error=pv_error)
        else:
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                flash("New account activated. Let's celebrate with a new blog post!")
                return redirect('/newpost')
            else:
                flash("That username already exists. Please pick a different name for your account.", 'error')
                return render_template('signup.html')
    else:
        return render_template('signup.html')



@app.route('/login', methods = ['POST', 'GET'])
def log_on():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = User.query.filter_by(username=username).first()
        if account and account.password == password:
            session['username'] = username
            flash("Hello again. Let's broadcast your thoughts to the world! 📡🌐")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            return render_template('login.html', username=username)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/')
def index():
    # TODO - show an index page with all users
    return render_template('index.html')


if __name__ == '__main__':
    app.run()