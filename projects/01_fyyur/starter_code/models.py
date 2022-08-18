import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    shows = db.relationship('Show', backref = 'venue', lazy = True, cascade = "all,delete", passive_deletes = True)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    # genres = db.Column(db.PickleType, nullable = True)
    genres = db.Column(db.ARRAY(db.String(120)))
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    def __repr__(self):
      return f'<Venue id={self.id} name={self.name}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, nullable = False)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    shows = db.relationship('Show', backref = 'artist', lazy = True, cascade = "all,delete", passive_deletes = True)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    # genres = db.Column(db.PickleType, nullable = True)
    genres = db.Column(db.ARRAY(db.String(120)))
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    def __repr__(self):
      return f'<Artist id={self.id} name={self.name}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE

class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key = True, nullable = False)
  start_time = db.Column(db.DateTime, nullable = False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable = False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable = False)
  created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
  def __repr__(self):
    return f'<show id={self.id} artist={self.artist_id} venue={self.venue_id}>'

# TODO: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# DONE