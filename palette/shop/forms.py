# -*- coding: utf-8 -*-
"""Shop forms."""
from flask_wtf import Form
from wtforms import StringField  # , DecimalField  # , IntegerField
from wtforms.validators import DataRequired

from palette.shop.models import Item


class ItemForm(Form):
    """Item form."""
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    terms = StringField('Terms')
    price = StringField('Price')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ItemForm, self).__init__(*args, **kwargs)
        self.item = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(ItemForm, self).validate()
        if not initial_validation:
            return False

        return True
