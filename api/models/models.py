from api.utils.errors import DatabaseProcessError, ValidationError
from datetime import datetime
import rethinkdb as rdb

r = rdb.RethinkDB()
connection = r.connect(db='biruda')


class RethinkDBModel(object):
    @classmethod
    def find(cls, id):
        return r.table(cls._table).get(id).run(conn)

    @classmethod
    def filter(cls, predicate):
        return list(r.table(cls._table).filter(predicate).run(conn))

    @classmethod
    def update(cls, id, fields):
        status = r.table(cls._table).get(id).update(fields).run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the update action")
        return True

    @classmethod
    def delete(cls, id):
        status = r.table(cls._table).get(id).delete().run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the delete action")
        return True

    @classmethod
    def update_where(cls, predicate, fields):
        status = r.table(cls._table).filter(predicate).update(fields).run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the update action")
        return True

    @classmethod
    def delete_where(cls, predicate):
        status = r.table(cls._table).filter(predicate).delete().run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the delete action")
        return True


class User(RethinkDBModel):
    _table = 'users'

    @classmethod
    def create(cls, **kwargs):
        firstname = kwargs.get('firstname')
        lastname = kwargs.get('lastname')
        email = kwargs.get('email')
        password = kwargs.get('password')
        confirmation_password = kwargs('confirmation_password')
        if password != password_confirmation:
            raise ValidationError("Password have to be equals to confirmation passoword")
        password = cls.hash_password(password)
        document = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'password': password,
            'created': datetime.now(r.make_timezone('+01:00')),
            'modified': datetime.now(r.make_timezone('+01:00'))
        }
        r.table(cls._table).insert(document).run(connection)

    @classmethod
    def validate(cls, email, password):
        docs = list(r.table(cls._table).filter({'email': email}).run(conn))

        if not len(docs):
            raise ValidationError("Could not find the e-mail address you specified")

        _hash = docs[0]['password']

        if cls.verify_password(password, _hash):
            try:
                token = jwt.encode({'id': docs[0]['id']}, current_app.config['SECRET_KEY'], algorithm='HS256')
                return token
            except JWTError:
                raise ValidationError("There was a problem while trying to create a JWT token.")
        else:
            raise ValidationError("The password you inputed was incorrect.")

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    def verify_password(password, _hash):
        return pbkdf2_sha256.verify(password, _hash)
