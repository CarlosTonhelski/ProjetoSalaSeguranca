class Config:

    SQLALCHEMY_DATABASE_URI = (
        'postgresql+psycopg2://postgres:admin123@127.0.0.1:5432/sala_seguranca'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False