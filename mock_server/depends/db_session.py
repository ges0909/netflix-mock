def db_session():
    from main import db

    with db.SessionLocal() as sess:
        yield sess
