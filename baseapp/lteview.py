from baseapp import app
from baseapp.models import Lte, Users
from baseapp.ltecontroller import LteController
from baseapp.lteform import LteForm
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask import render_template, request, redirect, url_for, abort
from baseapp.views import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/lte/<int:page_num>")
@login_required
def lte(page_num):
    lte = Lte.query.paginate(per_page=100, page=page_num, error_out=True)
    return render_template('lte.html', lte=lte)


@app.route('/lte/form', methods=["GET", "POST"])
@login_required
def lteform():
    form = LteForm()
    delete = request.args.get('delete', None)
    lid = request.args.get('lid', None)
    if form.validate_on_submit():
        ltec = LteController()
        lte = {}
        if form.delete.data == 'Y' and lid:
            lte['id'] = int(lid)
            ltec.delete(lte)
            return redirect(url_for('lte',page_num=1))
        else:
            lte['input'] = form.input.data
            lte['archive'] = form.archive.data
            lte['error'] = form.error.data
            lte['drop'] = form.drop.data
            lte['location'] = form.location.data
            lte['date'] = str(form.rdate.data)
            if lid:
                lte['id'] = int(lid)
                ltec.edit(lte)
            else:
                ltec.add(lte)

            return redirect(url_for('lte', page_num=1))

    if delete:
        form.delete.data = 'Y'
    else:
        form.delete.data = 'N'

    if lid:
        ltedata = Lte.query.filter_by(id=int(lid)).first()
        form.input.data = ltedata.input
        form.archive.data = ltedata.archive
        form.error.data = ltedata.error
        form.drop.data = ltedata.drop
        form.location.data = ltedata.location
        form.rdate.data =  datetime.strptime(ltedata.rdate, "%Y-%m-%d").date()

    return render_template('lteform.html', form=form, lid=lid)



