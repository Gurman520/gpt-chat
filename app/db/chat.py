from ..models import Conversation, Message


def get_conversations(current_user, db):
    return db.query(Conversation).filter(Conversation.user_id == current_user.id).all()

def create_conversation(conv, db):
    db.add(conv)
    db.commit()
    db.refresh(conv)

def get_conversation(current_user, conversation_id, db):
    return db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

def update_title(conv, new_title, db):
    conv.title = new_title
    db.commit()
    db.refresh(conv)

def get_messages(conversation_id, db):
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()

def create_message(msg, db):
    db.add(msg)
    db.commit()
    db.refresh(msg)
