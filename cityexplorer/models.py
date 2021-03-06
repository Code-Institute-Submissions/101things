""" Document Description """
from werkzeug.security import check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from cityexplorer import login_manager, mongo, app


class User():
    def __init__(self, _id, username, fname, lname, email, profile_img, is_admin):
        self._id = _id
        self.username = username
        self.fname = fname
        self.lname = lname
        self.email = email
        self.profile_img = profile_img
        self.is_admin = is_admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(hashed_password, password):
        return check_password_hash(hashed_password, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'email': self.email})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            email = s.loads(token)['email']
        except:
            return None
        return mongo.db.users.find_one({'email': email})

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_user(username):
    """ Defines how to locate & match the user model to the user object in
    the database """

    user = mongo.db.users.find_one({'username': username})
    if not user:
        return None
    return User(user['_id'], user['username'], user['fname'], user['lname'],
                user['email'], user['picture'], user['is_admin'])
