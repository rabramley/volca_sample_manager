import os
import simpleaudio as sa
import wave
import math
from datetime import datetime
from simpleaudio.shiny import PlayObject
from time import sleep
from flask import render_template, redirect, url_for, flash, current_app, request, session
from vsm.model import Bank
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


@blueprint.route("/banks/load", methods=['GET','POST'])
def bank_load():

    bank_id = request.args.get('bank_id', 0, type=int)
    bank = Bank.query.get_or_404(bank_id)    
    session['duration'] = wave_file_duration(bank.filepath)
    session['start_time'] = datetime.utcnow()

    os.system("amixer sset 'Headphone' 90%")

    wave = sa.WaveObject.from_wave_file(bank.filepath)
    player = wave.play()
    session['play_id'] = int(player.play_id)

    return {'bank_id': bank_id}


@blueprint.route("/banks/load_status")
def bank_load_status():

    player = PlayObject(int(session['play_id']))
    if player.is_playing():
        status = 'playing'
    else:
        status = 'not playing'

    time_elapsed = int((datetime.utcnow() - session['start_time']).total_seconds())
    percentage = int(time_elapsed * 100 / session['duration'])

    return {
        'duration': session['duration'],
        'elapsed': time_elapsed,
        'percentage': percentage,
        'status': status,
    }


@blueprint.route("/banks/stop")
def bank_stop():

    sa.stop_all()

    return redirect(url_for('ui.bank_index'))


def wave_file_duration(filename):
    f = wave.open(filename, 'rb')

    frames = f.getnframes()
    rate = f.getframerate()
    return int(math.ceil(frames / float(rate)))
