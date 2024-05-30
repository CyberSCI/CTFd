from flask import session
from flask_babel import lazy_gettext as _l
from wtforms import PasswordField, SelectField, StringField, TextAreaField
from wtforms.fields.html5 import DateField, URLField

from CTFd.constants.languages import SELECT_LANGUAGE_LIST
from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.forms.users import (
    attach_custom_user_fields,
    attach_user_bracket_field,
    build_custom_user_fields,
    build_user_bracket_field,
)
from CTFd.utils.countries import SELECT_COUNTRIES_LIST
from CTFd.utils.user import get_current_user, get_current_user_attrs


def SettingsForm(*args, **kwargs):
    class _SettingsForm(BaseForm):
        name = StringField("User Name")
        email = StringField("Email")
        password = PasswordField("Password")
        confirm = PasswordField("Current Password")
        affiliation = StringField("Affiliation")
        website = URLField("Website")
        country = SelectField("Region", choices=SELECT_COUNTRIES_LIST)
        submit = SubmitField("Submit")

        @property
        def extra(self):
            user = get_current_user_attrs()
            fields_kwargs = _SettingsForm.get_field_kwargs()
            return build_custom_user_fields(
                self,
                include_entries=True,
                fields_kwargs=fields_kwargs,
                field_entries_kwargs={"user_id": session["id"]},
            ) + build_user_bracket_field(self, value=user.bracket_id)

        @staticmethod
        def get_field_kwargs():
            user = get_current_user()
            field_kwargs = {"editable": True}
            if user.filled_all_required_fields is False:
                # Show all fields
                field_kwargs = {}
            return field_kwargs

    field_kwargs = _SettingsForm.get_field_kwargs()
    attach_custom_user_fields(_SettingsForm, **field_kwargs)
    attach_user_bracket_field(_SettingsForm)

    return _SettingsForm(*args, **kwargs)


class TokensForm(BaseForm):
    expiration = DateField(_l("Expiration"))
    description = TextAreaField("Usage Description")
    submit = SubmitField(_l("Generate"))
