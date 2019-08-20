import sys
import unittest

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

# Created a new FlaskGroup instance to extend the normal
# CLI with commands related to the Flask app.
app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    """
    Registers to the CLI so it can run from the command line
    to apply the model to the database
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Discovers and runs the tests"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command('seed_db')
def seed_db():
    """Populates the database with seed data."""
    db.session.add(User(username='cshannon1989', phone_number="(832) 865-8698"))
    db.session.add(User(username='fitzgerald', phone_number="(805) 444-4444"))
    db.session.commit()



if __name__ == "__main__":
    cli()
