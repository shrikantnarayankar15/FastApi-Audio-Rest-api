from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, PrimaryKeyConstraint
from .connection import Base

class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String)
    duration = Column(Integer)
    uploadTime = Column(DATETIME)

    def __init__(self, id, name, duration, uploadTime):
        self.id = id
        self.name = name
        self.duration = duration
        self.uploadTime = uploadTime

class Podcast(Base):
    __tablename__ = "podcast"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String)
    duration = Column(Integer)
    uploadTime = Column(DATETIME)
    host = Column(String)

class ParticipantPodcast(Base):
    __tablename__ = 'participant_Podcast'

    id = Column(Integer,ForeignKey("podcast.id"))
    participantName = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint(
            id,
            participantName),
        {})

class Audiobook(Base):
    __tablename__ = 'audiobook'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String)
    author = Column(String)
    narrator = Column(String)
    duration = Column(Integer)
    uploadTime = Column(DATETIME)
