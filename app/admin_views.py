from flask import redirect, url_for, request
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from .extensions import db, admin
from .models import Enquiry, Shipment, User


class SecureAccessMixin:
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))


class SecureModelView(SecureAccessMixin, ModelView):
    pass


class SecureIndexView(SecureAccessMixin, AdminIndexView):
    pass


admin.add_view(SecureModelView(Enquiry, db.session))
admin.add_view(SecureModelView(Shipment, db.session))
admin.add_view(SecureModelView(User, db.session))