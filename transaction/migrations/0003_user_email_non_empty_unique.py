from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transaction", "0002_unique_user_email"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE auth_user
                DROP CONSTRAINT IF EXISTS auth_user_email_unique;

                CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_non_empty_unique
                ON auth_user (email)
                WHERE email <> '';
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]