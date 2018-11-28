from flask import render_template, redirect, url_for
from kamericanapp.database import bp_database
import kamericanapp.database.forms
from kamericanapp.database.models import Image
from kamericanapp.database.logic import DatabaseManager
from kamericanapp import db
from sqlalchemy.orm.exc import MultipleResultsFound

from rq import Queue
from redis import Redis

@bp_database.route('/database', methods=['GET', 'POST'])
def route_database():
    """Route to Database Management page."""
    # Load forms
    load_images_form = kamericanapp.database.forms.LoadImagesForm()
    resize_images_form = kamericanapp.database.forms.ResizeImagesForm()

    # Database manager
    database_manager = DatabaseManager()
    original_image_path_list = database_manager.get_image_glob_list(database_manager.original_dir_path)
    resize_image_path_list = database_manager.get_image_glob_list(database_manager.resize_dir_path)
    images_to_resize_query_list = Image.query.filter(Image.filepath_resize == None).all()

    if load_images_form.submit_load.data and load_images_form.validate_on_submit():
        # Load new images into db
        db_load_images(original_image_path_list)

        return redirect(url_for('database.route_database'))
    elif resize_images_form.submit_resize.data and resize_images_form.validate_on_submit():
        # Create new resized images
        redis = Redis()
        queue = Queue(connection=redis)

        queue.enqueue_call(
            func=async_resize_images,
            args=(images_to_resize_query_list,),
        )
        return redirect(url_for('database.route_database'))
    else:
        return render_template(
            template_name_or_list='database.html',
            load_images_form=load_images_form,
            n_original_images=len(original_image_path_list),
            n_database_images=Image.query.count(),
            resize_images_form=resize_images_form,
            n_resize_images=len(resize_image_path_list),
            n_resize_filepath_images=Image.query.count() - len(images_to_resize_query_list),
        )

def db_load_images(original_image_path_list):
    '''Load new images into the database.'''
    has_new_images = False
    for original_image_path in original_image_path_list:
        #print("Processing:", original_image_path.name)
        try:
            # Check if there are duplicate filenames already in db
            image_filename_query_match = Image.query.filter_by(filename=original_image_path.name).one_or_none()
            #print("Query:", image_filename_query_match)
        except MultipleResultsFound as error:
            # There's an image with the same filename in db
            # @@@@@ add stuff here to fix the duplication @@@@@@@@@@@@@
            print("Error:", error)
            print("Multiple images found in database with the same filename:", original_image_path.name)
        else:
            # One or no images with same filename have been found in db
            if image_filename_query_match:
                # Current image already in db
                print("Already in database:", original_image_path.name)
            else:
                # Add image to db
                has_new_images = True
                print("Adding to database:", original_image_path.name)
                image = Image()
                image.filename = original_image_path.name
                image.filepath_original = original_image_path
                db.session.add(image)
    if has_new_images:
        print("Committing database additions")
        db.session.commit()
    return
def async_resize_images(images_to_resize_query_list):
    database_manager = DatabaseManager()
    result = database_manager.resize_images(images_to_resize_query_list)
    return result