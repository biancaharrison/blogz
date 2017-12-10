from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.Text())

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry



@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']
        new_blog = Blog(title, entry)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", blogs=blogs)


@app.route('/new-post')
def newpost():
    return render_template('newpost.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')





if __name__ == '__main__':
    app.run()