import asyncio
import uuid

import bcrypt
import typer
from db.models.auth_requests.user_request import UserRequest
from db.postgres import PostgresProvider
from services.models.signup import SignupModel

app = typer.Typer()


async def create_superuser(email: str, password: str):
    postgres = PostgresProvider()
    try:
        model = SignupModel(
            password=password,
            first_name='',
            last_name='',
            email=email
        )
        password_hash = bcrypt.hashpw(model.password.encode(), bcrypt.gensalt())
        request = UserRequest(
            uuid=str(uuid.uuid4()),
            email=model.email,
            password=password_hash,
            first_name=model.first_name,
            last_name=model.last_name,
            is_superuser=True,
            is_verified=True
        )
        result = await postgres.add_single_data(request, 'user')
        if result['status_code'] == 201:
            print(f"Superuser {email} created")
        else:
            print(f"Error: {result['content']}")
    except Exception as e:
        print(f"Error: {e}")


@app.command()
def create(email: str, password: str):
    asyncio.run(create_superuser(email, password))


if __name__ == "__main__":
    app()
