from baseapp.models import Lte
from baseapp import db

class LteController:
    def add(self, ltedata):
        existing = Lte.query.filter_by(input=ltedata['input'],rdate=ltedata['date'],location=ltedata['location']).first()
        if not existing:
            lte = Lte()
            lte.input = ltedata['input']
            lte.archive = ltedata['archive']
            lte.error = ltedata['error']
            lte.drop = ltedata['drop']
            lte.rdate = ltedata['date']
            lte.location = ltedata['location']
            db.session.add(lte)
            db.session.commit()
            return True

        return False

    def edit(self, ltedata):
        lte = Lte.query.filter_by(id=ltedata['id']).first()
        if lte:
            lte.input = ltedata['input']
            lte.archive = ltedata['archive']
            lte.error = ltedata['error']
            lte.drop = ltedata['drop']
            lte.rdate = ltedata['date']
            lte.location = ltedata['location']
            db.session.commit()
            return True

        return False

    def delete(self, ltedata):
        lte = Lte.query.filter_by(id=ltedata['id']).first()
        if lte:
            db.session.delete(lte)
            db.session.commit()
            return True

        return False
