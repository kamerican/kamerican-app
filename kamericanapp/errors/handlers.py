from flask import render_template
from kamericanapp import db
from kamericanapp.errors import bp_errors


@bp_errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@bp_errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
