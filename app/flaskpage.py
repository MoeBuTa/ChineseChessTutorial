from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'data_posted': 'April 20,2018'
    },
    {
        'author': 'Wei Yang',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'data_posted': 'April 21,2018'
    }

]


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', posts=posts, title='NBA')


@app.route("/about")
def about():
    return "<h1>About page</h1>"


if __name__ == '__main__':
    app.run(debug=True)