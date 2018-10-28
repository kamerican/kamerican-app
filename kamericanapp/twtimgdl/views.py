from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from kamericanapp import db
from kamericanapp.database.models import Users
from kamericanapp.twtimgdl import bp


@bp.route('/launch', methods=['GET', 'POST'])
@login_required
def launch():
    if current_user.perm_twtimgdl:
        return render_template('launch.html')
    else:
        flash("You do not have permission to access Twitter Image Downloader.")
        return redirect(url_for('main.index'))
    





