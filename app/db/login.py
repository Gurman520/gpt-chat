from ..models import User


def get_user(user, db):
    return db.query(User).filter(User.username == user.username).first()

def create_user(db_user, db):
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
