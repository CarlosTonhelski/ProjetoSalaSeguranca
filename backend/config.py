class Config:

    SQLALCHEMY_DATABASE_URI = (
        'postgresql+psycopg2://postgres:admin123@10.1.25.39:5432/sala_seguranca'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False