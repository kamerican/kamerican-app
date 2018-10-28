from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from kamericanapp import db
from kamericanapp.twtimgdl import bp
from kamericanapp.twtimgdl.forms import LinksForm
from kamericanapp.twtimgdl.logic import ImageDownloader
import time

@bp.route('/twtimgdl', methods=['GET', 'POST'])
@login_required
def twtimgdl():
    if not current_user.perm_twtimgdl:
        flash("You do not have permission to access Twitter Image Downloader.")
        return redirect(url_for('main.index'))
        
    else:
        form = LinksForm()
        if form.validate_on_submit():
            time_start = time.time()
            total_number_of_images = 0

            twitter_URL_list = form.links.data.splitlines()

            image_downloader = ImageDownloader()

            for twitter_URL in twitter_URL_list:
                image_downloader.Download(twitter_URL)
                total_number_of_images += 1
            

            
            time_end = time.time()
            print("Wrote " + str(total_number_of_images) + " images to disk.")
            print("Process took " + str(time_end - time_start) + " seconds.")
            return redirect(url_for('main.index'))
        else:
            return render_template('twtimgdl.html', form=form)
    





