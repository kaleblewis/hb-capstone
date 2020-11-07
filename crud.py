"""CRUD operations."""

from model import db, User, Preference, QueryHistory, connect_to_db
import datetime


def create_user(name, email, password):
    """Create and return a new user.

    >>> create_user('jane', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    >>> create_user('', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    >>> create_user('jane', '', 'password1')
    # TODO: update docstring

    >>> create_user('jane', 'jane.doe@email.com', '')
    # TODO: update docstring

    user cannot pass a name that's other than alpha chars
    >>> create_user('1', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    >>> create_user('@', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    user cannot pass an email that's not an email
    >>> create_user('jane', 'jane.doe', 'password1')
    # TODO: update docstring

    >>> create_user('jane', 'janedoe@emailcom', 'password1')
    # TODO: update docstring

    >>> create_user('jane', '@.', 'password1')
    # TODO: update docstring

    name cannot be > 50 chars:
    >>> create_user('jane12345678901234156789012345678901234567890123415678901234567890123456789012345', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    email cannot be > 80 chars:
    >>> create_user('jane', 'jane.doe@email.com123456789012341567890123456789012345678901234156789012345678901', 'password1')
    # TODO: update docstring

    password cannot be > 20 chars:
    >>> create_user('jane', 'jane.doe@email.com', 'password1234567890123')
    # TODO: update docstring

    """
    
    user = User(fname=name, 
                email=email, 
                password=password,
                user_since = datetime.datetime.now())

    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(id):
    """Return a user by primary key.
    
    >>> get_user_by_id(1)
    <User id=1 email=jane.doe@email.com>
    """

    return User.query.get(id)


def get_user_by_email(email):

    return User.query.filter(User.email == email).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)