import random
from datetime import timedelta
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_firstname():
        return faker.first_name()

    @staticmethod
    def generate_lastname():
        return faker.last_name()

    @staticmethod
    def generate_total_price():
        return random.randint(100, 5000)

    @staticmethod
    def generate_deposit_paid():
        return faker.boolean()

    @staticmethod
    def generate_checkin_date():
        return faker.date_between(start_date='today', end_date='+30d')

    @staticmethod
    def generate_checkout_date(checkin_date):
        return checkin_date + timedelta(days=random.randint(1, 14))

    @staticmethod
    def generate_additional_needs():
        options = ["Breakfast", "Lunch", "Dinner", "Late checkout", "Extra bed", ""]
        return random.choice(options)

    @staticmethod
    def generate_random_password():
        return faker.password()

    @staticmethod
    def generate_random_name():
        return faker.name()

    @staticmethod
    def generate_movie_name():
        return faker.sentence(nb_words=3)

    @staticmethod
    def generate_movie_description():
        return faker.text(max_nb_chars=200)

    @staticmethod
    def generate_image_url():
        return faker.image_url()

    @staticmethod
    def generate_location():
        return random.choice(["MSK", "SPB"])

    @staticmethod
    def generate_genre_id():
        return random.randint(5, 100)
