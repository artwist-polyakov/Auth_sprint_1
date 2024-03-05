import uuid

import typer

app = typer.Typer()


@app.command()
def generate():
    print(uuid.uuid4())


if __name__ == "__main__":
    app()
