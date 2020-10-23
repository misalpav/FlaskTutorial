from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default='Anon')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

#
# all_posts = [
#     {
#         'title': 'This is the title of post 1',
#         'content': 'This is the content in all posts'
#     }
#
# ]*4
#
# all_posts.append(
#     {
#         'title': 'This is the title of post 1',
#         'content': 'This is the content in all posts',
#         'author':'Kishore'
#     }
#
# )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET','POST'])
def posts():

    if request.method == 'POST':
        p_title = request.form['title']
        p_content = request.form['content']
        new_post = BlogPost(title=p_title, content=p_content, author=request.form['author'])
        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts')

    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/home/users/<string:name>/posts/<int:idno>')
def hello(name, idno):
    return "Hello, {}! This is your post {}".format(name, idno)


@app.route('/onlyget', methods=['GET'])
def get_req():
    return 'You can only get this webpage.'


if __name__ == '__main__':
    app.run(debug=True)
