from flask import request
from extensions import db

from RAManagementSuite.models import ProfileForm


def create_user_profile(user_id):
    # Retrieve user data from the form submission
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    birthdate = request.form.get('birthdate')
    phonenumber = request.form.get('phonenumber')
    gender = request.form.get('gender')
    pronouns = request.form.get('pronouns')
    major = request.form.get('major')
    addressline1 = request.form.get('addressline1')
    addressline2 = request.form.get('addressline2')
    postcode = request.form.get('postcode')
    city = request.form.get('city')
    province = request.form.get('province')
    shift_availability = request.form.get('shift_availability')

    # Create a new profile instance
    profile = ProfileForm(
        user_id=user_id,
        firstname=firstname,
        lastname=lastname,
        birthdate=birthdate,
        phonenumber=phonenumber,
        gender=gender,
        pronouns=pronouns,
        major=major,
        addressline1=addressline1,
        addressline2=addressline2,
        postcode=postcode,
        city=city,
        province=province,
        shift_availability=shift_availability
    )

    # Add the profile to the database
    db.session.add(profile)
    db.session.commit()
