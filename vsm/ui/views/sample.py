from flask import render_template, redirect, url_for
from .. import blueprint

@blueprint.route("/samples")
def sample_index():
    return render_template("sample/index.html")

