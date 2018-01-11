from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dSxeFR{SM7h5D!Qw'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, entry, owner):
        self.title = title
        self.entry = entry
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner') 

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if username.strip() == "":
            flash("Invalid username", "error")
        
        if password.strip() == "":
            flash("Invalid password", "error")

        if user and user.password != password:
            flash("Invalid password", "error")            
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/new-post')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if len(username.strip()) < 3:
            flash("That's not a valid username", "error")

        if len(password.strip()) < 3:
            flash("That's not a valid passowrd", "error")

        if password != verify:
            flash("Passwords do not match", "error")

        if len(username.strip()) >= 3 and len(password.strip()) >= 3 and password == verify:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/new-post')          
            else:
                flash("Username already exists", "error")
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog')
def blog():
    
    blog_id = request.args.get('id')
    blog_user = request.args.get('user')

    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('blog_entry.html', blog=blog)
    
    if blog_user:
        user_id = User.query.filter_by(username=blog_user).first()
        blogs = Blog.query.filter_by(owner_id=user_id.id).all()

        return render_template('singleUser.html', user=user_id, blogs=blogs)

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
            owner = User.query.filter_by(username=session['username']).first()
            new_blog = Blog(request.form['title'], request.form['entry'], owner)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id
            return redirect('/blog?id={0}'.format(blog_id))
        
        return render_template('newpost.html', title=title, entry=entry, title_error=title_error, entry_error=entry_error)
    
    return render_template('newpost.html')
    
        

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html',title="Build A Blog", users=users)


if __name__ == '__main__':
    app.run()