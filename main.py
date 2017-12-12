from flask import Flask, request, redirect, render_template, url_for
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


@app.route('/blog')
def blog():
    
    blog_id = request.args.get('id')
    
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('blog_entry.html', blog=blog)

    blogs = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", blogs=blogs)


@app.route('/new-post', methods=['POST', 'GET'])
def newpost(): 

    title_error = ""
    entry_error = ""

    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']
            
        if title.strip() == "":
            title_error = "Please fill in the title"
        
        if entry.strip() == "":
            entry_error = "Please fill in the body"

        if title_error == "" and entry_error == "":
            new_blog = Blog(request.form['title'], request.form['entry'])
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/')
        
        return render_template('newpost.html', title=title, entry=entry, title_error=title_error, entry_error=entry_error)
    
    return render_template('newpost.html')
    
        

@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", blogs=blogs)


if __name__ == '__main__':
    app.run()