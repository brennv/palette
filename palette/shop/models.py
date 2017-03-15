# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from palette.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Item(SurrogatePK, Model):
    """An item to be created by a user."""

    __tablename__ = 'items'
    name = Column(db.String(80), nullable=False)
    description = Column(db.String(255))  #
    terms = Column(db.String(255))
    price = Column(db.String(80))
    is_active = Column(db.Boolean(), default=True)
    created_at = Column(db.DateTime, default=dt.datetime.utcnow)
    user_id = reference_col('users')  # , nullable=True)
    user = relationship('User', backref='items')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        # return '<Item({name})>'.format(name=self.name)
        return str(id)


class Images(SurrogatePK, Model):
    """An image to be added to an item."""

    __tablename__ = 'images'
    image = Column(db.String(80), nullable=False)
    caption = Column(db.String(80))
    is_primary = Column(db.Boolean(), default=False)
    item_id = reference_col('items')  # , nullable=True)
    item = relationship('Item', backref='images')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, image=image, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Image({caption})>'.format(caption=self.caption)


class Reviews(SurrogatePK, Model):
    """A review to be added to an item."""

    __tablename__ = 'reviews'
    stars = Column(db.Integer(), nullable=False)
    comment = Column(db.String(255))
    is_active = Column(db.Boolean(), default=True)
    created_at = Column(db.DateTime, default=dt.datetime.utcnow)  # server_default=text('now()'
    item_id = reference_col('items')  # , nullable=True)
    item = relationship('Item', backref='reviews')
    user_id = reference_col('users')  # , nullable=True) for anon reviews
    user = relationship('User', backref='reviews')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, stars=stars, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Image({stars})>'.format(stars=self.stars)
