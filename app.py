from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models.blogpost import BlogPost
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 



@app.before_first_request
def create_database():
    db.create_all()

@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.filter_by(id = post_id).one()

    date_posted = post.date_posted.strftime('%B %d  %Y')
    return render_template('post.html', post=post, date_posted=date_posted)

@app.route('/add')
def contact():
    return render_template('add.html')

@app.route('/addpost', methods = ['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = BlogPost(title=title, subtitle=subtitle, author=author,date_posted=datetime.now(), content=content)

    db.session.add(post)
    db.session.commit()


    return redirect('/')



if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(debug=True)