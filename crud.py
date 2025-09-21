from sqlalchemy.orm import Session
from models import File

def create_file(db: Session, filename: str, content: bytes):
    db_file = File(filename=filename, content=content)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_files(db: Session):
    return db.query(File).all()
