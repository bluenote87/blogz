from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

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

@app.route("/blog")
def view_a_post():
    post_id = request.args.get('id')
    if post_id:
        post = Blog.query.filter_by(id=post_id).first()
        return render_template('viewpost.html', post=post,
            title = "You are viewing a single post")
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
    # TODO - let users register to the site
    return ""


@app.route('/login', methods = ['POST', 'GET'])
def log_on():
    # TODO - let users sign into previously created accounts
    return ""


@app.route('/index')
def index():
    # TODO - show an index page with all users
    return ""


if __name__ == '__main__':
    app.run()