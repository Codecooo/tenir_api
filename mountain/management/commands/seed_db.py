import random
from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from hiker.models import Capability
from mountain.models import AlertLevel, DifficultyLevel, Mountain, MountainPicture
from transaction.models import Hiker, Ticket, TransactionStatus, Trip, Transaction
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Seed database untuk data fake realistis."

    def handle(self, *args, **options):
        self.stdout.write("Clearing old data...")
        Transaction.objects.all().delete()
        Ticket.objects.all().delete()
        Trip.objects.all().delete()
        Hiker.objects.all().delete()
        MountainPicture.objects.all().delete()
        Mountain.objects.all().delete()

        fake = Faker('id_ID')
        Faker.seed(676767)

        self.stdout.write("Seeding Users...")
        # Create a default test user if one doesn't exist
        test_user, _ = User.objects.get_or_create(
            username="testuser",
            defaults={
                "email": "testuser@example.com",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        test_user.set_password("password123")
        test_user.save()
        
        self.stdout.write("Seeding Mountains...")
        indonesian_mountains = [
            ("Gunung Rinjani", "Lombok, NTB", 3726),
            ("Gunung Bromo", "Probolinggo, Jawa Timur", 2329),
            ("Gunung Semeru", "Lumajang, Jawa Timur", 3676),
            ("Gunung Gede", "Cianjur, Jawa Barat", 2958),
            ("Gunung Prau", "Wonosobo, Jawa Tengah", 2565),
            ("Gunung Merbabu", "Magelang, Jawa Tengah", 3145),
        ]

        created_mountains = []
        for name, location, height in indonesian_mountains:
            mountain = Mountain.objects.create(
                name=name,
                location=location,
                description=fake.paragraph(nb_sentences=3),
                height=Decimal(height),
                difficulty_level=random.choice(DifficultyLevel.values),
                region="Indonesia",
                indonesian_weekday_price=Decimal(random.choice([15000, 20000, 25000])),
                indonesian_weekend_price=Decimal(random.choice([25000, 35000, 50000])),
                international_weekday_price=Decimal(random.choice([150000, 200000])),
                international_weekend_price=Decimal(random.choice([250000, 300000])),
                alert_level=random.choice(AlertLevel.values),
                main_image="https://thumb.wikimedia.org/wikipedia/commons/thumb/6/68/Mt_Masurai_%28201293087%29.jpeg/330px-Mt_Masurai_%28201293087%29.jpeg?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail",
                is_favorite=fake.boolean(chance_of_getting_true=30),
                is_volcanic_active=fake.boolean(chance_of_getting_true=60),
            )
            created_mountains.append(mountain)

        self.stdout.write("Seeding Hikers...")
        created_hikers = []
        for _ in range(25):
            hiker = Hiker.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                identity_number=fake.bothify(text="317101########"),  
                phone_number=fake.bothify(text="08##########"),
                emergency_contact_name=fake.name(),
                emergency_contact_phone=fake.bothify(text="08##########"),
                capability_level=random.choice(Capability.values),
            )
            created_hikers.append(hiker)

        self.stdout.write("Seeding Trips...")
        created_trips = []
        for mountain in created_mountains:
            for i in range(2):
                start_date = timezone.now().date() + timedelta(days=random.randint(5, 60))
                end_date = start_date + timedelta(days=random.randint(2, 4))
                trip = Trip.objects.create(
                    name=f"Open Trip {mountain.name} Vol. {i + 1}",
                    mountain=mountain,
                    start_date=start_date,
                    end_date=end_date,
                )
                created_trips.append(trip)

        self.stdout.write("Seeding Transactions & Tickets...")
        for trip in created_trips:
            # Select 2-5 random hikers per trip
            trip_hikers = random.sample(created_hikers, k=random.randint(2, 5))
            price_per_ticket = trip.mountain.indonesian_weekend_price

            tickets = []
            for hiker in trip_hikers:
                ticket = Ticket.objects.create(
                    hiker=hiker,
                    price_paid=price_per_ticket
                )
                tickets.append(ticket)

            # Create Transaction linking tickets
            transaction = Transaction.objects.create(
                user=test_user,
                trip=trip,
                total_amount_paid=price_per_ticket * len(tickets),
                status=random.choice(TransactionStatus.values),
            )
            transaction.tickets.set(tickets)

        self.stdout.write(self.style.SUCCESS("Database successfully seeded with realistic test data!"))