from flask import render_template, redirect, url_for
from kamericanapp.database import bp_database
from kamericanapp.database.forms import LoadImagesForm
from kamericanapp.database.models import Image
from kamericanapp.database.logic import DatabaseManager
from kamericanapp import db
import os

@bp_database.route('/database', methods=['GET', 'POST'])
def route_database():
    """Route to Database Management page."""
    database_manager = DatabaseManager()
    
    load_image_path_list = database_manager.get_image_glob_list(database_manager.load_dir_path)
    
    
    
    form = LoadImagesForm()
    if form.validate_on_submit():
        # @@@@@@@@@@ add an if statement here later to check if the list is empty @@@@@@@2
        for load_image_path in load_image_path_list:
            #print(load_image_path.name)
            #continue
            image_query_list = Image.query.filter_by(filename=load_image_path.name).all()
            print("Query:", image_query_list)
            if not image_query_list:
                # Add load image to db and move the image file to the original directory
                original_image_path = database_manager.original_dir_path / load_image_path.name
                #print("{0} -> {1}".format(load_image_path, original_image_path))
                #print(load_image_path.is_file())
                if original_image_path.is_file():
                    print("@@@ {} already exists in original directory @@@".format(original_image_path.name))
                else:
                    load_image_path.rename(original_image_path)
            else:
                # There's an image with the same filename in the db, so move the current image into the duplicate directory
                if len(image_query_list) > 1:
                    print("@@@ There's a duplicate image in the database @@@")
                else:
                    pass
        return redirect(url_for('database.route_database'))
    else:
        return render_template(
            'database.html',
            form=form,
            n_load_images=len(load_image_path_list),
        )
    




    
    
    
    