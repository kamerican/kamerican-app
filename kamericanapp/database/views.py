from flask import render_template, redirect, url_for
from kamericanapp.database import bp_database
from kamericanapp.database.forms import LoadImagesForm
from kamericanapp.database.models import Image
from kamericanapp.database.logic import DatabaseManager
from kamericanapp import db

@bp_database.route('/database', methods=['GET', 'POST'])
def route_database():
    """Route to Database Management page."""
    database_manager = DatabaseManager()
    n_load_images = database_manager.get_n_load_images()
    #print(n_load_images)


    
    form = LoadImagesForm()
    if form.validate_on_submit():
        # do stuff
        return redirect(url_for('database.route_database'))
    else:
        return render_template(
            'database.html',
            form=form,
            n_load_images=n_load_images,
        )
    




    
    
    
    