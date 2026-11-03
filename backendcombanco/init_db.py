from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.database import engine, SessionLocal
from app.models import Base, Usuario, Perfil
from app.security import hash_password


def initialize_database():
    print("Iniciando configuração do banco de dados...")

    Base.metadata.create_all(bind=engine)

    if not settings.create_initial_admin:
        print("Criação do administrador inicial desabilitada.")
        return

    if not settings.initial_admin_password:
        raise ValueError(
            "INITIAL_ADMIN_PASSWORD precisa ser configurada."
        )

    db = SessionLocal()

    try:
        existing = db.scalar(
            select(Usuario).where(
                Usuario.email == settings.initial_admin_email
            )
        )

        if existing:
            print("Administrador inicial já existe.")
            return

        admin = Usuario(
            nome="Administrador",
            email=settings.initial_admin_email,
            senha_hash=hash_password(settings.initial_admin_password),
            perfil=Perfil.ADMIN
        )

        db.add(admin)

        try:
            db.commit()
            print("Administrador inicial criado com sucesso.")

        except IntegrityError:
            db.rollback()

            existing = db.scalar(
                select(Usuario).where(
                    Usuario.email == settings.initial_admin_email
                )
            )

            if existing:
                print("Administrador já foi criado por outra execução.")
            else:
                raise

    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()