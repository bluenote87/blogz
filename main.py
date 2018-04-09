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

@app.route("/blog", methods = ['POST', 'GET'])
def index():

    title_error = ""
    body_error = ""
    posts = Blog.query.all()
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        
        if blog_title == "":
            title_error = "I need something in the title before posting!"
        if blog_body == "":
            body_error = "I need something in the body before posting!"
        if title_error or body_error:
            return render_template('blog.html', title="My Awesome Dynamic Blog", posts=posts, 
                title_redux = blog_title, body_redux = blog_body, title_error=title_error, body_error=body_error)
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            posts = Blog.query.all()
            return render_template('blog.html', title="My Awesome Dynamic Blog", posts=posts, 
                title_redux = "", body_redux = "", title_error=title_error, body_error=body_error)

    if request.method == 'GET':
        return render_template('blog.html', title="My Awesome Dynamic Blog", posts=posts, 
                title_redux = "", body_redux = "", title_error=title_error, body_error=body_error)
    

    

@app.route('/newpost', methods = ['GET'])
def add_a_post():

    return redirect('blog')

if __name__ == '__main__':
    app.run()