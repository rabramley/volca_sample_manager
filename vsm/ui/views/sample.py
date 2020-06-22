import os
from flask import render_template, redirect, url_for, send_file, flash
from vsm.model import Sample
from .. import blueprint, db
from ..forms import SampleUploadForm, SampleLoadForm


@blueprint.route("/samples")
def sample_index():
    upload_form = SampleUploadForm()
    load_form = SampleLoadForm()

    samples = Sample.query.order_by(Sample.created_datetime.desc()).paginate(
        page=1, per_page=5, error_out=False
    )

    return render_template("sample/index.html", samples=samples, upload_form=upload_form, load_form=load_form)


@blueprint.route("/samples/upload", methods=['POST'])
def sample_upload():
    upload_form = SampleUploadForm()

    if upload_form.validate_on_submit():

        files_filenames = []

        for sample in upload_form.samples.data:
            s = Sample(filename=sample.filename)

            db.session.add(s)
            db.session.flush()

            os.makedirs(os.path.dirname(s.filepath), exist_ok=True)
            sample.save(s.filepath)

        db.session.commit()
    else:
        flash('Invalid sample upload')

    return redirect(url_for('ui.sample_index'))


@blueprint.route("/samples/load", methods=['POST'])
def sample_load():
    load_form = SampleLoadForm()

    if load_form.validate_on_submit():
        sample = Sample.query.get_or_404(load_form.id.data)

    else:
        flash('Invalid sample load')

    return redirect(url_for('ui.sample_index'))


@blueprint.route("/samples/<int:id>/file")
def sample_file(id):
    sample = Sample.query.get_or_404(id)

    return send_file(sample.filepath, attachment_filename=sample.filename)
