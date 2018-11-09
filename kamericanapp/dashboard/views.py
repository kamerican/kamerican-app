from flask import render_template, flash, redirect, url_for
from kamericanapp.dashboard import bp_dashboard

@bp_dashboard.route('/')
def root():
    flash('Redirected to index!')
    return redirect(url_for('dashboard.index'))

@bp_dashboard.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')





