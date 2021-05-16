from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, status
from fastapi import Depends
from pydantic import ValidationError
from pydantic.types import SecretBytes
from sqlalchemy.orm import Session
from starlette.routing import request_response
from starlette.status import HTTP_400_BAD_REQUEST
from config.enums import AudioFiles
from schemas import schemas
from database import models
from database.crud import audiobook, song, podcast
from database import connection


router = APIRouter(tags=['Audios'])

@router.get('/{typeFile}', status_code=200)
async def getAudio(typeFile: AudioFiles, db: Session = Depends(connection.get_db)):
    
    if typeFile==AudioFiles.Song:
        connection = song.Song(db)
        return connection.display()   
            
    if typeFile==AudioFiles.Podcast:
        connection = podcast.Podcast(db)
        return connection.display()
        
    if typeFile==AudioFiles.Audiobook:
        connection = audiobook.Audiobook(db)
        return connection.display()
    
    return {'data':f'returning {typeFile}'}


@router.get('/{typeFile}/{id}', status_code=200)
async def getAudioWithId(typeFile: AudioFiles, id:int=None, db: Session = Depends(connection.get_db)):
    
    if typeFile==AudioFiles.Song:
        connection = song.Song(db)
        result = connection.display(id)   
            
    if typeFile==AudioFiles.Podcast:
        connection = podcast.Podcast(db)
        result = connection.display(id)
        
    if typeFile==AudioFiles.Audiobook:
        connection = audiobook.Audiobook(db)
        result = connection.display(id)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'Error':f'Id {id} {typeFile} not Found'})
    return result


@router.post('/{typeFile}', status_code=status.HTTP_200_OK)
async def createAudio(typeFile: AudioFiles, audioFileMetadata: dict, db: Session = Depends(connection.get_db)):
    
    try:
        if typeFile==AudioFiles.Song:
            validatedItem = schemas.Song(**audioFileMetadata)
            connection = song.Song(db)
            connection.create(validatedItem)

        if typeFile==AudioFiles.Podcast:
            validatedItem = schemas.Podcast(**audioFileMetadata)
            connection = podcast.Podcast(db)
            connection.create(validatedItem)

        if typeFile==AudioFiles.Audiobook:
            validatedItem = schemas.Audiobook(**audioFileMetadata)
            connection = audiobook.Audiobook(db)
            connection.create(validatedItem)

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
    
    return {"Details":"Success"}


@router.put('/{typeFile}/{id}', status_code=200)
async def update(typeFile: AudioFiles, audioFileMetadata:dict, id:int=None, db: Session = Depends(connection.get_db), ):

    if typeFile==AudioFiles.Song:
        validatedItem = schemas.Song(**audioFileMetadata)
        connection = song.Song(db)
        result = connection.update(id, validatedItem)   
            
    if typeFile==AudioFiles.Podcast:
        validatedItem = schemas.Podcast(**audioFileMetadata)
        connection = podcast.Podcast(db)
        result = connection.update(id, validatedItem)
        
    if typeFile==AudioFiles.Audiobook:
        validatedItem = schemas.Audiobook(**audioFileMetadata)
        connection = audiobook.Audiobook(db)
        result = connection.update(id, validatedItem)
        
    
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'Error':f'Id {id} {typeFile} not Found'})

    return result

@router.delete('/{typeFile}/{id}', status_code=200)
async def delete(typeFile: AudioFiles, id:int=None, db: Session = Depends(connection.get_db)):

    if typeFile==AudioFiles.Song:
        connection = song.Song(db)
        result = connection.delete(id)   
            
    if typeFile==AudioFiles.Podcast:
        connection = podcast.Podcast(db)
        result = connection.delete(id)
        
    if typeFile==AudioFiles.Audiobook:
        connection = audiobook.Audiobook(db)
        result = connection.delete(id)
        
    print(result)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'Error':f'Id {id} {typeFile} not Found'})

    return result