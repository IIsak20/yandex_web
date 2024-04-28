from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feed.db'
db = SQLAlchemy(app)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')



@app.route('/prices')
def price():
    return render_template('price.html')


@app.route('/feeds', methods=['POST', 'GET'])
def feeds():
    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']

        post = Post(name=name, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/feedback')
        except:
            return 'При добавлении отзыва произошла ошибка'

    else:
        return render_template('feeds.html')


@app.route('/feedback')
def feedback():
    feedback = Post.query.all()
    return render_template('feedback.html', feedback=feedback)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='127.0.0.1')
