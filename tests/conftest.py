import pytest

from project.config import TestingConfig
from project.dao.main import UserMoviesDAO, DirectorsDAO, GenresDAO, MoviesDAO, UserDAO
from project.models import User, Movie, UserMovies, Director, Genre
from project.server import create_app
from project.services import GenresService
from project.services.auth_service import AuthService
from project.services.favorites_service import UserMoviesService
from project.services.user_service import UsersService
from project.setup.db import db as database
from project.tools.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()

    yield database

    database.session.close()


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def directors_dao(db):
    return DirectorsDAO(db.session)


@pytest.fixture
def users_movies_dao(db):
    return UserMoviesDAO(db.session)


@pytest.fixture
def genres_dao(db):
    return GenresDAO(db.session)


@pytest.fixture
def movies_dao(db):
    return MoviesDAO(db.session)


@pytest.fixture
def users_dao(db):
    return UserDAO(db.session)


@pytest.fixture
def users_service(users_dao, genres_dao):
    return UsersService(user_dao=users_dao, genre_dao=genres_dao)


@pytest.fixture
def directors_service(directors_dao):
    return GenresService(dao=directors_dao)


@pytest.fixture
def genres_service(genres_dao):
    return GenresService(dao=genres_dao)


@pytest.fixture
def auth_service(users_service):
    return AuthService(user_service=users_service)


@pytest.fixture
def movies_service(movies_dao):
    return GenresService(dao=movies_dao)

@pytest.fixture
def user_movie_service(users_movies_dao, users_service, movies_service):
    return UserMoviesService(users_movies_dao, users_service, movies_service)


@pytest.fixture
def user_1(db):
    password = generate_password_hash('1111')
    obj = User(email="email_1", password=password)
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def user_2(db):
    password = generate_password_hash('2222')
    obj = User(email="email_2", password=password)
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def movie_1(db):
    m = Movie(
        title='????????????????_1',
        description='????????????????_1',
        trailer='??????????????_1',
        year=1,
        rating=5.5,
        genre_id=1,
        director_id=1
    )
    db.session.add(m)
    db.session.commit()
    return m


@pytest.fixture
def movie_2(db):
    m = Movie(
        title='????????????????_2',
        description='????????????????_2',
        trailer='??????????????_2',
        year=2,
        rating=2.5,
        genre_id=2,
        director_id=2
    )
    db.session.add(m)
    db.session.commit()
    return m


@pytest.fixture
def movie_3(db):
    m = Movie(
        title='????????????????_3',
        description='????????????????_3',
        trailer='??????????????_3',
        year=3,
        rating=3.3,
        genre_id=3,
        director_id=3
    )
    db.session.add(m)
    db.session.commit()
    return m


@pytest.fixture
def director_1(db):
    d = Director(name="????????????????_1")
    db.session.add(d)
    db.session.commit()
    return d


@pytest.fixture
def director_2(db):
    d = Director(name="????????????????_2")
    db.session.add(d)
    db.session.commit()
    return d


@pytest.fixture
def genre_1(db):
    g = Genre(name="????????????")
    db.session.add(g)
    db.session.commit()
    return g


@pytest.fixture
def genre_2(db):
    g = Genre(name="??????????????")
    db.session.add(g)
    db.session.commit()
    return g


@pytest.fixture
def favorite_1(db, user_1, movie_1):
    f = UserMovies(
        user_id=user_1.id,
        movie_id=movie_1.id
    )
    db.session.add(f)
    db.session.commit()
    return f


@pytest.fixture
def favorite_2(db, user_2, movie_2):
    f = UserMovies(
        user_id=user_2.id,
        movie_id=movie_2.id
    )
    db.session.add(f)
    db.session.commit()
    return f


@pytest.fixture
def headers(user_1, auth_service):
    tokens = auth_service.generate_token(user_1.email, '1111')
    access_token = tokens['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}'}
    return headers
