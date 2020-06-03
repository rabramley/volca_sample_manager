import os
import simpleaudio as sa
from flask import render_template, redirect, url_for, flash, current_app
from vsm.model import Bank
from vsm.celery import celery
from .. import blueprint, db
from ..forms import BankUploadForm

@blueprint.route("/banks",)
def bank_index():
    upload_form = BankUploadForm()

    banks = Bank.query.order_by(Bank.created_datetime.desc()).paginate(
        page=1, per_page=5, error_out=False
    )

    return render_template("bank/index.html", banks=banks, upload_form=upload_form)


@blueprint.route("/banks/upload", methods=['POST'])
def bank_upload():
    upload_form = BankUploadForm()

    if upload_form.validate_on_submit():
        b = Bank(
            name=upload_form.name.data,
            filename=upload_form.upload.data.filename,
        )

        db.session.add(b)
        db.session.flush()

        os.makedirs(os.path.dirname(b.filepath), exist_ok=True)
        upload_form.upload.data.save(b.filepath)

        db.session.commit()
    else:
        flash('Invalid bank upload')

    return redirect(url_for('ui.bank_index'))


@blueprint.route("/banks/<int:id>/load")
def bank_load(id):

    sa.stop_all()

    bank = Bank.query.get_or_404(id)

    load_bank.delay(id)

    return redirect(url_for('ui.bank_index'))


@blueprint.route("/banks/stop")
def bank_stop():

    sa.stop_all()

    return redirect(url_for('ui.bank_index'))


@celery.task()
def load_bank(id):
    current_app.logger.info(f'load_bank: id={id}')

    bank = Bank.query.get(id)

    current_app.logger.info(f'load_bank: playing {bank.filepath}')

    wave_obj = sa.WaveObject.from_wave_file(bank.filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

    current_app.logger.info(f'load_bank: finished {bank.filepath}')

