from flask import redirect, url_for, request
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from .extensions import db, admin

from .models import Enquiry, Shipment, User,CourierRate
from .constants import ENQUIRY_STATUSES, SHIPMENT_STATUSES


class SecureAccessMixin:
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))


class SecureModelView(SecureAccessMixin, ModelView):
    pass


class SecureIndexView(SecureAccessMixin, AdminIndexView):
    pass


class EnquiryAdmin(SecureModelView):

    column_formatters = {
        "status": lambda view, context, model, name:
            f"{model.status}"
    }

    form_choices = {
        "status": [(s, s) for s in ENQUIRY_STATUSES]
    }

    column_searchable_list = ["name", "contact"]
    column_filters = ["status", "country"]


class ShipmentAdmin(SecureModelView):

    form_choices = {
        "status": [(s, s) for s in SHIPMENT_STATUSES]
    }

    column_searchable_list = ["tracking_id", "name", "contact"]
    column_filters = ["status", "country", "created_at"]


admin.add_view(
    EnquiryAdmin(Enquiry, db.session)
)
admin.add_view(ShipmentAdmin(Shipment, db.session))
admin.add_view(SecureModelView(User, db.session))
admin.add_view(
    SecureModelView(CourierRate, db.session)
)