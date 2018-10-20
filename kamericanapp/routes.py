from flask import render_template, flash, redirect
from kamericanapp import app
from kamericanapp.forms import LoginForm

@app.route('/')
def RedirectToIndex():
    return redirect('/index')

@app.route('/index')
def Index():
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

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            'Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)







if __name__ == "__main__":
    app.run(debug=True)