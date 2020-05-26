from flask import render_template, redirect, url_for
from .. import blueprint

@blueprint.route("/banks")
def bank_index():
    return render_template("bank/index.html")
