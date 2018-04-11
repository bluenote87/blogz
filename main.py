from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:alwaysbecoding@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def go_to_home():
    return redirect('/blog')

@app.route("/blog")
def index():
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
        
        if blog_title == "":
            title_error = "I need something in the title before posting!"
        if blog_body == "":
            body_error = "I need something in the body before posting!"
        if title_error or body_error:
            return render_template('newpost.html', title="My Awesome Dynamic Blog", 
                title_redux = blog_title, body_redux = blog_body, title_error=title_error, body_error=body_error)
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            posts = Blog.query.all()
            return render_template('blog.html', title="My Awesome Dynamic Blog", posts=posts)
    else:
        return render_template('newpost.html', title="My Awesome Dynamic Blog", 
            title_redux = "", body_redux = "", title_error=title_error, body_error=body_error)


if __name__ == '__main__':
    app.run()