from flask import Blueprint, render_template, redirect, url_for,flash
from .extensions import db
from .models import Enquiry, Shipment,CourierRate
from .forms import EnquiryForm, TrackForm
from flask_login import login_required
bp = Blueprint("main", __name__)


@bp.route("/enquiry", methods=["GET", "POST"])
def enquiry():
    form = EnquiryForm()
    form.country.choices = [
        (rate.country, rate.country)
        for rate in CourierRate.query.order_by(CourierRate.country).all()
    ]

    if form.validate_on_submit():
        new_enquiry = Enquiry(
            name=form.name.data,
            contact=form.contact.data,
            pickup_location=form.pickup_location.data,
            drop_location=form.drop_location.data,
            country=form.country.data,
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


@bp.route("/admin/enquiry/<int:enquiry_id>/convert", methods=["POST"])
@login_required
def convert_enquiry(enquiry_id):
    enquiry = db.get_or_404(Enquiry, enquiry_id)

    # 2. Prevent converting the same enquiry twice
    if enquiry.status != "pending":
        flash("This enquiry has already been converted.")
        return redirect(url_for("main.enquiry"))

    # 3. Find the courier rate using the country
    rate = CourierRate.query.filter_by(
        country=enquiry.country
    ).first()

    # 4. Make sure a rate exists
    if not rate:
        flash("No courier rate found for this country.")
        return redirect(url_for("main.enquiry"))

    # 5. Calculate estimated price
    estimated_price = rate.price_per_kg * enquiry.weight

    # 6. Generate tracking ID
    import random

    while True:
        tracking_id = f"VV-2026-{random.randint(1000, 9999)}"

        existing = Shipment.query.filter_by(
            tracking_id=tracking_id
        ).first()

        if not existing:
            break

    # 7. Create shipment
    shipment = Shipment(
        enquiry_id=enquiry.id,
        name=enquiry.name,
        contact=enquiry.contact,
        pickup_location=enquiry.pickup_location,
        drop_location=enquiry.drop_location,
        country=enquiry.country,
        weight=enquiry.weight,
        estimated_price=estimated_price,
        parcel_details=enquiry.parcel_details,
        tracking_id=tracking_id
    )

    # 8. Add shipment
    db.session.add(shipment)

    # 9. Update enquiry status
    enquiry.status = "converted"

    # 10. Save everything
    db.session.commit()

    flash(f"Enquiry converted successfully. Tracking ID: {tracking_id}")

    return redirect(url_for("main.enquiry"))

