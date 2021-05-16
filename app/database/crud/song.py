from .. import models
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class Song:
    def __init__(self, db):
        self.db = db
    
    def create(self, result):
        try:
            
            result = result.dict()
            result = models.Song(**result)
            self.db.add(result)
            self.db.commit()
            self.db.refresh(result)

        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Exist")
        

    def display(self, id=None):
        if not id:
            return self.db.query(models.Song).all()
        else:
            return self.db.query(models.Song).filter(models.Song.id == id).first()
    
    def update(self, id, request):
        song = self.db.query(models.Song).filter(models.Song.id == id)
        if not song.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")
        song.update(request.dict())
        self.db.commit()
        return {f'updated {id}'}


    def delete(self, id=None):
        song = self.db.query(models.Song).filter(models.Song.id == id).delete(synchronize_session=False)
        if song:
            self.db.commit()
            return {f'deleted {id}'}
        else:
            return None