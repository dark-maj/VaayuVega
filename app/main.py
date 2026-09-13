from flask import Blueprint, render_template, redirect, url_for
from .extensions import db
from .models import Enquiry, Shipment
from .forms import EnquiryForm, TrackForm

bp = Blueprint("main", __name__)


@bp.route("/enquiry", methods=["GET", "POST"])
def enquiry():
    form = EnquiryForm()
    if form.validate_on_submit():
        new_enquiry = Enquiry(
            name=form.name.data,
            contact=form.contact.data,
            pickup_location=form.pickup_location.data,
            drop_location=form.drop_location.data,
            weight=form.weight.data,
            parcel_details=form.parcel_details.data,
            estimated_price=None,
        )
        db.session.add(new_enquiry)
        db.session.commit()

        return redirect(
            url_for("main.enquiry_confirmation", enquiry_id=new_enquiry.id)
        )

    return render_template("enquiry.html", form=form)


@bp.route("/enquiry/confirmation/<int:enquiry_id>")
def enquiry_confirmation(enquiry_id):
    # Not a trackable ID — just the enquiry's own reference, shown once,
    # so the customer has something to quote if they contact Dad directly.
    # Guest tracking only starts once Dad converts this into a Shipment.
    submitted = Enquiry.query.get_or_404(enquiry_id)
    return render_template("confirmation.html", enquiry=submitted)


@bp.route("/track", methods=["GET", "POST"])
def track_lookup():
    form = TrackForm()
    if form.validate_on_submit():
        tracking_id = form.tracking_id.data.upper()
        return redirect(url_for("main.track_result", tracking_id=tracking_id))

    return render_template("track_lookup.html", form=form)


@bp.route("/track/<tracking_id>")
def track_result(tracking_id):
    tracking_id = tracking_id.upper()
    shipment = Shipment.query.filter_by(tracking_id=tracking_id).first_or_404()
    return render_template("track_result.html", shipment=shipment)
