from baseapp import *
from baseapp.models import Users
from werkzeug.security import generate_password_hash

db.create_all()

admin = Users.query.filter_by(username='admin').first()
if not admin:
    hashed_password = generate_password_hash('123*45', method='sha256')
    new_user = Users(username='admin', password=hashed_password,admin=True)
    db.session.add(new_user)
    print("user 'admin' created!")

print("Users 'admin' already set!")
db.session.commit()
