from flask import request
from extensions import db

from models import ProfileForm


def create_blank_user_profile(user_id):
    user_profile = ProfileForm(user_id=user_id)
    db.session.add(user_profile)
    db.session.commit()


def create_user_profile(user_id, firstname, lastname, birthdate,
                        phonenumber, gender, pronouns, major,
                        addressline1, addressline2, postcode,
                        city, province, shift_availability):
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


def edit_user_profile(id, user_id, firstname, lastname, birthdate,
                      phonenumber, gender, pronouns, major,
                      addressline1, addressline2, postcode,
                      city, province, shift_availability):

    profile = ProfileForm.query.filter_by(id=id).first()

    # update the fields
    profile.user_id = user_id
    profile.firstname = firstname,
    profile.lastname = lastname,
    profile.birthdate = birthdate,
    profile.phonenumber = phonenumber,
    profile.gender = gender,
    profile.pronouns = pronouns,
    profile.major = major,
    profile.addressline1 = addressline1,
    profile.addressline2 = addressline2,
    profile.postcode = postcode,
    profile.city = city,
    profile.province = province,
    profile.shift_availability = shift_availability

    # save the changes
    db.session.commit()

