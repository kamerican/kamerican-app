from flask import render_template, flash, redirect, url_for, request
from kamericanapp import db
from kamericanapp.imagedownloader import bp
from kamericanapp.imagedownloader.forms import LinksForm
from kamericanapp.imagedownloader.logic import ImageDownloader
import time

@bp.route('/imagedownloader', methods=['GET', 'POST'])
def imagedownloader():
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
        return redirect(url_for('dashboard.index'))
    else:
        return render_template('imagedownloader.html', form=form)
    





