import random

import click
from werkzeug.security import generate_password_hash

from app import fake, db
from app.auth.models import User


@click.command(name="seeder")
@click.option('--count', default=1)
def add_users(count):
    """
    Generate fake users.
    """
    random_public_id = []
    random_first_name = []
    random_last_name = []
    random_email = []
    random_password = []

    # Ensure we get the count number of usernames.

    for i in range(0, count):
        random_public_id.append(fake.uuid4())
        random_first_name.append(fake.first_name())
        random_last_name.append(fake.last_name())
        random_email.append(fake.email())
        random_password.append(random.randint(11111111, 99999999))

    random_public_id = list(set(random_public_id))
    random_first_name = list(set(random_first_name))
    random_last_name = list(set(random_last_name))
    random_email = list(set(random_email))
    random_password = list(set(random_password))

    while True:
        if len(random_public_id) == 0:
            break

        public_id = random_public_id.pop()
        first_name = random_first_name.pop()
        last_name = random_last_name.pop()
        email = random_email.pop()
        password = generate_password_hash(str(random_password.pop()))

        user = User(public_id, first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()

    return print('{} users were added successfully to the database.'.format(count))
