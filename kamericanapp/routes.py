from flask import render_template
from kamericanapp import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'kamerican'}
    posts = [
        {
            'author': {'username': 'test1'},
            'body': '123'
        },
        {
            'author': {'username': 'test2'},
            'body': '456'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)



if __name__ == "__main__":
    app.run(debug=True)



