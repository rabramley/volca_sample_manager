import os
from flask import render_template, redirect, url_for
from vsm.model import Bank
from .. import blueprint, db
from ..forms import BankUploadForm

@blueprint.route("/banks", methods=['GET', 'POST'])
def bank_index():
    upload_form = BankUploadForm()

    banks = Bank.query.order_by(Bank.created_datetime.desc()).paginate(
        page=1, per_page=5, error_out=False
    )

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

        return redirect(url_for('ui.bank_index'))

    return render_template("bank/index.html", banks=banks, upload_form=upload_form)


@blueprint.route("/banks")
def bank_upload():
    return render_template("bank/index.html")


@blueprint.route("/banks")
def bank_add():
    return render_template("bank/index.html")
