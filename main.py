import os
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from http import HTTPStatus
from flask_migrate import Migrate

class Config():
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://root:1234@localhost/moviedatabase2"

class DevlopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://root:1234@localhost/moviedatabase2"

class ProductionConfig(Config):
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://","postgresql://",1)
    SQLALCHEMY_DATABASE_URI = uri

env = os.environ.get("ENV","Devlopment" )

if env == "Production":
    config_str = ProductionConfig
else:
    config_str = DevlopmentConfig


app = Flask(__name__)
api = Api(app)

app.config.from_object(config_str)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:welcome$1234@localhost/moviesdb"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://root:1234@localhost/moviedatabase2"

db = SQLAlchemy(app)

migrate = Migrate(app,db)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    # static method for adding movie
    @staticmethod
    def add_movie(title,year,genre):
        new_movie = Movie(title=title, year=year, genre=genre)
        db.session.add(new_movie)
        db.session.commit()

    # static method for getting all movies in table
    @staticmethod
    def get_movie():
       return Movie.query.all()

    # static method for getting one movie in table by id
    @staticmethod
    def get_one_movie(id):
        return Movie.query.filter_by(id=id).first()

    # static method for deleting one movie in table
    @staticmethod
    def delete_movie(id):
        delete_movie = Movie.query.filter_by(id=id).delete()
        db.session.commit()
        return delete_movie

    # static method for UPDATING 1 movie DEATIL in table
    @staticmethod
    def update_movie(id, title, year, genre):
        update_movie = Movie.query.filter_by(id=id).first()
        print(update_movie)
        update_movie.title = title
        update_movie.year = year
        update_movie.genre = genre
        db.session.commit()
        return update_movie

# Class for all movies funtion
class AllMovies(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        Movie.add_movie(title=data["title"], year=data["year"], genre=data["genre"])
        return jsonify(data)

    def get(self):
        data = Movie.get_movie()
        print(data)
        movie_list = []
        print(movie_list)
        for i in data:
            temp_dict= {"title":i.title, "year":i.year, "genre":i.genre}
            movie_list.append(temp_dict)
            print(movie_list)
        return jsonify(movie_list)

# Class for one movie funtion
class oneMovie(Resource):
    # using filetr by
     def get(self,id):
            data= Movie.get_one_movie(id)
            print(data)
            if data:
                print(data.id)
                print(data.title)
                print(data.year)
                print(data.genre)
                return jsonify({"title":data.title , "year":data.year, "genre":data.year},{"status":HTTPStatus.OK})
            else:
                # return ({"message":"ID not found","status":404})
                return ({"message": "ID not found", "status": HTTPStatus.NOT_FOUND})

     def delete(self,id):
            data = Movie.delete_movie(id)
            print(data)
            if data:
                return HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND

     def put(self,id):
            data = request.get_json()
            print(data)
            Movie.update_movie(id, data["title"], data["year"], data["genre"])
            if data:
                return jsonify({"title":data["title"] , "year":data["year"], "genre":data["genre"]},{"status":HTTPStatus.OK})
            else:
                return HTTPStatus.NOT_FOUND

# Class for one movie funtion using for
class oneMovieFor(Resource):
    def get (self,id):
        data = Movie.get_movie()
        print(data)
        movie_list = []
        for i in data:
            print(i)
            if i.id == id:
                movie_list.append({"title":i.title , "year":i.year, "genre":i.year})
                return movie_list
        else:
            return ({"message":"ID not found"})

api.add_resource(AllMovies,"/movies")
api.add_resource(oneMovie,"/movies/<int:id>")
api.add_resource(oneMovieFor,"/onemovie/<int:id>")

if __name__ == "__main__":
    app.run()