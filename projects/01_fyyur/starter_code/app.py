#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import collections
from models import db, Venue, Show, Artist
import datetime
import config
from os import abort
import sys

collections.Callable = collections.abc.Callable
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
# db = SQLAlchemy(app)

migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
# DONE

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # date = dateutil.parser.parse(value)
  if isinstance(value, str):
      date = dateutil.parser.parse(value)
  else:
      date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
 
  all_cities_states = set()
  all_venues = Venue.query.all()
  for venue in all_venues:
      all_cities_states.add((venue.city,venue.state))
  cities = []
  for city,state in all_cities_states:
    cities.append({
      "city":city,
      "state":state,
      "venues":[]
    })
    for venue in all_venues:
      for city_object in cities:
        if venue.city ==city_object.get('city') and venue.state == city_object.get('state'):
            upcoming_shows = len(Show.query.join(Venue).filter(Show.start_time > datetime.datetime.utcnow()).all())
            city_object['venues'].append({
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows": upcoming_shows
            })
  return render_template('pages/venues.html', areas=cities);

  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  # return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_query = request.form.get('search_term') # get search query
  search_result = Venue.query.filter(Venue.name.ilike('%' + search_query + '%')).all() # get venue by query results
  search_array= []

  for data in search_result:
    num_upcoming_shows= Show.query.filter(Show.venue_id == data.id).count() 
    search_array.append({
      "id":data.id,
      "name":data.name,
     "num_upcoming_shows":num_upcoming_shows 
    })
  response={
    "count": len(search_array),
    "data": search_array
  }

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.filter(Venue.id == venue_id ).first()
  past_shows_all = Show.query.join(Venue, Show.venue_id == venue_id).filter(Show.start_time <= datetime.datetime.utcnow()).all()
  upcoming_shows_all = Show.query.join(Venue, Show.venue_id == venue_id).filter(Show.start_time > datetime.datetime.utcnow()).all()
     

  past_shows=[] #prepare list of past shows
  for show in past_shows_all:
    past_shows.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link":show.artist.image_link,
      "start_time": show.start_time
    })
  
  #prepare list of upcoming shows
  upcoming_shows=[]
  for show in upcoming_shows_all:
    upcoming_shows.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link":show.artist.image_link,
      "start_time": show.start_time
    })

# prepare data object for artist
  data ={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address":venue.address,
    "city":venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link":venue.facebook_link,
    "seeking_talent":venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows":  past_shows,
    "upcoming_shows":   upcoming_shows,
    "past_shows_count":len(past_shows),
    "upcoming_shows_count":len(upcoming_shows), 
  }
  return render_template('pages/show_venue.html', venue=data)
 
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # DONE
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link')
  image_link = request.form.get('image_link')
  website = request.form.get('website_link')
  seeking_description = request.form.get('seeking_description')
  seeking_talent = True if request.form.get('seeking_talent') =='y' else False 

  venue_form =VenueForm(request.form)
  if venue_form.validate():
    try:
      new_venue = Venue(
                        name=name,
                        seeking_description=seeking_description,
                        city=city,
                        state=state,
                        address=address,
                        phone=phone,
                        genres=genres,
                        facebook_link=facebook_link,
                        website=website,
                        image_link=image_link,
                        seeking_talent=seeking_talent
                        )
      db.session.add(new_venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + new_venue.name + ' was successfully listed!')
    except:
      db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + new_venue.name+ ' could not be listed.','error')
    finally:
      db.session.close()
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      return render_template('pages/home.html')
  else:
    flash('Form Inputs Invalid please check again')
    return render_template('forms/new_venue.html', form=venue_form)



@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  
  print('delete venue from ' + venue_id)
  venue = Venue.query.filter(Venue.id == venue_id).first()
  
  try:
    for show in venue.shows:
      db.session.delete(show)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was deleted')
  except:
    db.session.rollback()
    flash("Error deleting venue")
  finally:
    db.session.close()
  
  
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # DONE
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # DONE
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)


  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_query = request.form.get('search_term') # get search query
  search_result = Artist.query.filter(Artist.name.ilike('%' + search_query + '%')).all() # get artist by query results
  search_array= []
  for data in search_result:
    search_array.append({
      "id":data.id,
      "name":data.name,
    })

  response={
    "count": len(search_array),
    "data": search_array
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

# ----------------------------------------------------------------------------------------


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.filter(Artist.id == artist_id).first()
  past_shows_all = Show.query.join(Artist, Show.artist_id == artist.id).filter(Show.start_time <= datetime.datetime.utcnow()).all()
  upcoming_shows_all = Show.query.join(Artist, Show.artist_id == artist.id).filter(Show.start_time > datetime.datetime.utcnow()).all()

  past_shows=[] #prepare list of past shows
  for show in past_shows_all:
    past_shows.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link":show.venue.image_link,
      "start_time": show.start_time
    })
  
  upcoming_shows=[]
  for show in upcoming_shows_all:
    upcoming_shows.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link":show.venue.image_link,
      "start_time": show.start_time
    })

# prepare data object for artist
  data ={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows) 
  }
  return render_template('pages/show_artist.html', artist=data)

# --------------------------------------------------------------------------------------
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter(Artist.id==artist_id).first()
  form = ArtistForm()
  form.name.data = artist.name
  form.genres.data  = artist.genres
  form.city.data  = artist.city
  form.state.data  = artist.state
  form.phone.data  = artist.phone
  form.image_link.data  = artist.image_link
  form.facebook_link.data  = artist.facebook_link
  form.seeking_venue.data  = artist.seeking_venue
  form.seeking_description.data  =artist.seeking_description
  form.website_link.data = artist.website

  return render_template('forms/edit_artist.html', form=form, artist=artist)
 
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  # DONE

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist_form =  ArtistForm(request.form)
  artist = Artist.query.filter(Artist.id==artist_id).first()

  if(artist_form.validate()):
    artist.name = artist_form.name.data
    artist.genres = artist_form.genres.data
    artist.city = artist_form.city.data
    artist.state =artist_form.state.data
    artist.phone = artist_form.phone.data
    artist.image_link = artist_form.image_link.data
    artist.facebook_link = artist_form.facebook_link.data
    artist.seeking_description = artist_form.seeking_description.data
    artist.website = artist_form.website_link.data
    artist.seeking_venue = artist_form.seeking_venue.data
    try:
      db.session.commit()
      flash(f'update to artist {artist.name} successful')
    except:
      db.session.rollback()
      flash('an error occurred while updating')
    finally:
      db.session.close()
    return redirect(url_for('show_artist',artist_id=artist.id))
  else:
    flash('Some fields are Invalid please fill correctly')

  return redirect(url_for('show_artist', artist_id=artist.id))

  
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter(Venue.id==venue_id).first()
  form.name.data = venue.name
  form.genres.data  = venue.genres
  form.city.data  = venue.city
  form.address.data = venue.address
  form.state.data  = venue.state
  form.phone.data  = venue.phone
  form.image_link.data  = venue.image_link
  form.facebook_link.data  = venue.facebook_link
  form.seeking_talent.data  = venue.seeking_talent
  form.seeking_description.data  =venue.seeking_description
  form.website_link.data = venue.website
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)
 
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  # DONE
 

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.filter(Venue.id==venue_id).first() # find the venue to be edited
  venue_form =  VenueForm(request.form)
  

  if(venue_form.validate()):
    venue.name = venue_form.name.data
    venue.genres = venue_form.genres.data
    venue.city = venue_form.city.data
    venue.state =venue_form.state.data
    venue.address = venue_form.address.data
    venue.phone = venue_form.phone.data
    venue.image_link = venue_form.image_link.data
    venue.facebook_link = venue_form.facebook_link.data
    venue.seeking_description = venue_form.seeking_description.data
    venue.website = venue_form.website_link.data
    venue.seeking_talent = venue_form.seeking_talent.data
    try:
      db.session.commit()
      flash(f'update to venue {venue.name} successful')
    except:
      db.session.rollback()
      flash('There was an error while updating')
    finally:
      db.session.close()
    return redirect(url_for('show_venue',venue_id=venue.id))
  else:
    flash('Invalid field! Please check and fill correctly')
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link')
  image_link = request.form.get('image_link')
  website = request.form.get('website_link')
  seeking_description = request.form.get('seeking_description')
  seeking_venue = True if request.form.get('seeking_talent') =='y' else False 
  
  # validate form data
  artist_form =ArtistForm(request.form)
  
  if artist_form.validate():
    # TODO: modify data to be the data object returned from db insertion
    try:
      new_artist = Artist(
                          name=name,
                          seeking_description=seeking_description,
                          city=city, state=state, phone=phone,
                          genres=genres,
                          facebook_link=facebook_link,
                          website=website,
                          image_link=image_link,
                          seeking_venue=seeking_venue
                          )
      db.session.add(new_artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + new_artist.name + ' was successfully listed!')
    except:
      db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist ' + new_artist.name+ ' could not be listed.')
    finally:
      db.session.close()
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')
  else:
    flash('Invalid form inputs. Please check and try again')
    return render_template('forms/new_artist.html', form=artist_form)
 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  data=[]
  for show in Show.query.filter(Show.artist_id != None).filter(Show.venue_id != None ).all(): 
    new_show = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link":show.artist.image_link,
      "start_time": show.start_time
    }
    data.append(new_show)
  return render_template('pages/shows.html', shows=data)

  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')
  new_show = Show(artist_id=artist_id, venue_id=venue_id,start_time=start_time)

  show_form = ShowForm(request.form)


  if show_form.validate():
    try:
      db.session.add(new_show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
    return render_template('pages/home.html')
  else:
    flash('Invalid form input, please check and try again')
    return render_template('forms/new_show.html', form=show_form)

  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
