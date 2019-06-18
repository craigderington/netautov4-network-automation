from netauto import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship


# Define application db.Models

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password = Column(String(256), nullable=False)
    active = Column(Boolean, default=1)
    email = Column(String(120), unique=True, nullable=False)
    last_login = Column(DateTime)
    login_count = Column(Integer)
    fail_login_count = Column(Integer)
    created_on = Column(DateTime, default=datetime.now, nullable=True)
    changed_on = Column(DateTime, default=datetime.now, nullable=True)
    created_by_fk = Column(Integer)
    changed_by_fk = Column(Integer)

    def __repr__(self):
        if self.last_name and self.first_name:
            return '{} {}'.format(
                self.first_name,
                self.last_name
            )


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        if self.id and self.text:
            return "{} {}".format(
                self.id,
                self.text
            )


class Locations(db.Model):
    """
    Class instance for Store
    """
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        if self.id:
            return "{}".format(str(id))


class Alerts(db.Model):
    """
    Class instance for Alerts
    """
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now, nullable=False)
    category = Column(String(50), nullable=False)
    message_id = Column(Integer)
    message_type = Column(String(50), nullable=False)
    message_scope = Column(String(50), nullable=False)
    message_status = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    urgency = Column(String(50), nullable=True)
    severity = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    information_url = Column(String(500), nullable=True)
    sys_mod_count = Column(Integer)
    updated = Column(DateTime, default=datetime.now, nullable=False)
    sender_id = Column(Integer)
    metric_name = Column(String(50), nullable=True)
    certainty = Column(String(50), nullable=True)

    def __repr__(self):
        if self.category, self.created, self.message_status, self.description:
            return '{} {} {} {}'.format(
                self.category,
                self.created,
                self.message_status,
                self.description
            )
        return self.id
