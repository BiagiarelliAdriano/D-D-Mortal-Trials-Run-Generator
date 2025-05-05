from flask.cli import FlaskGroup
from app import app, db  # make sure your app and db are imported from your app module
from flask_migrate import Migrate

migrate = Migrate(app, db)

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
