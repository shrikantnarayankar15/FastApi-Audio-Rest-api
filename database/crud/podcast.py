from sqlalchemy.orm.session import Session
from .. import models
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class Podcast:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, request):
        try:
            result = request.dict()
            participants = result['participants']
            id =  result['id']
            result.pop('participants')
            
            result = models.Podcast(**result)
            self.db.add(result)
            self.db.commit()
            self.db.refresh(result)

            self.create_participants(id, participants)
            
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Exist")
    
    def create_participants(self,id, participants):
        buffer = []
            
        for participant in participants:
            buffer.append(models.ParticipantPodcast(id=id, participantName=participant))

        self.db.bulk_save_objects(buffer)
        self.db.commit()

    def display(self, id=None):
        if not id:
            results = self.db.query(models.Podcast).all()
            result_participants = self.db.query(models.ParticipantPodcast).all()
            
            perIdParticipant = {}

            for result in result_participants:

                if result.id not in perIdParticipant:
                    perIdParticipant[result.id] = []
                perIdParticipant[result.id].append(result.participantName)
                    

            for result in results:
                result.participants = perIdParticipant[result.id]

            
        if id:
            results = self.db.query(models.Podcast).filter(models.Podcast.id == id).first()
            if not results:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")

            result_participants = self.db.query(models.ParticipantPodcast).filter(models.ParticipantPodcast.id == id)
            participants = []
            for participant in result_participants:
                participants.append(participant.participantName)
            results.participants = participants

        return results
    
    def update(self, id, request):
        podcast = self.db.query(models.Podcast).filter(models.Podcast.id == id)

        if not podcast.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")

        result = request.dict()
        participants = result['participants']
        result.pop('participants')

        id = result['id']
        self.delete_participant(id)
        self.create_participants(id, participants)

        podcast.update(result)
        self.db.commit()
        return request
        

    def delete_participant(self, id):
        self.db.query(models.ParticipantPodcast).filter(models.ParticipantPodcast.id == id).delete(synchronize_session=False)

    def delete(self, id):
        podcast = self.db.query(models.Podcast).filter(models.Podcast.id == id).delete(synchronize_session=False)
        self.delete_participant(id)
        
        if podcast:
            self.db.commit()
            return {f'deleted {id}'}
        else:
            return None