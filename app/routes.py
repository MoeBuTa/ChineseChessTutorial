from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    # This function takes a template filename and a variable list of template arguments and
    # returns the same template, but with all the placeholders in it replaced with actual values.
    return render_template('index.html', title='Chinese Chess')


# GET requests return information to the client (the web browser in this case)
#  All the requests in the application so far are of this type

# POST requests are typically used when the browser submits form data to the server
# (in reality GET requests can also be used for this purpose, but it is not a recommended practice)
@app.route('/loginAndRegister', methods=['GET', 'POST'])
def login_and_register():
    form = LoginForm()

    # do all the form processing work. GET:False POST:Ture
    if form.validate_on_submit():

        # show a message to the user
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('loginAndRegister.html', title='Sign In & up', form=form)


