from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from kamericanapp import db
from kamericanapp.database.models import Users
from kamericanapp.dashboard import bp


@bp.route('/')
def root():
    return redirect(url_for('dashboard.index'))

@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')





