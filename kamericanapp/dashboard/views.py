from flask import render_template, flash, redirect, url_for
from kamericanapp.dashboard import bp_dashboard

@bp_dashboard.route('/')
def route_root():
    """Route to root."""
    flash('Redirected to index!')
    return redirect(url_for('dashboard.route_index'))

@bp_dashboard.route('/index', methods=['GET', 'POST'])
def route_index():
    """Route to index."""
    return render_template('index.html')





