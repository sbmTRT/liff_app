import time
import json

from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from db import engine, session , Base
from utils.log_utils import *


# Generate a Fernet key
key = Fernet.generate_key()

# Ensure the key is URL-safe base64-encoded
url_safe_key = key.decode('utf-8')
cipher_suite = Fernet(url_safe_key)

# Timeout setting
timeout = 1800

table_name = 'SESSION_MANAGEMENT'

class Session(Base):
    __tablename__ = table_name

    SESSION_ID   = Column('SESSION_ID',   String(60),   primary_key=True)
    SESSION_DATA = Column('SESSION_DATA', String(4000), nullable=True)
    ACCESS_TIME  = Column('ACCESS_TIME',  DateTime,     nullable=True)

Session.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)


# encrypt JSON data
async def encrypt_data(data: dict):
    json_data = json.dumps(data)
    encrypted_data = cipher_suite.encrypt(json_data.encode())
    return encrypted_data


# decrypt the encrypted JSON data
async def decrypt_data(encrypted_data: bytes):
    decrypted_data = cipher_suite.decrypt(encrypted_data.decode())
    json_data = json.loads(decrypted_data)
    return json_data


# Get Session Id
async def get_session_id(session_id: UUID = None):
    if session_id == None:
        session_id = uuid4()
    return session_id


# Session Start
async def session_start():
    session_id = await get_session_id()
    ses_str_data = json.dumps({})
    current_time = time.time()

    response = await create_session(session_id, ses_str_data)

    if response:
        return session_id
    else:
        return False


# Session Create
async def create_session(session_id = None, session_data = None) -> bool:
    if session_id is None:
        put_info('[create_session]'+'session_id is not set')
        return False

    if isinstance(session_id, UUID):
        session_id = str(session_id)

    if session_data is None:
        put_info('[create_session]'+'key is not set')
        return False

    try:
        access_time  = datetime.now()
        session_data = await encrypt_data(session_data)

        # Insert seesion data
        new_session = Session(SESSION_ID=session_id, SESSION_DATA=session_data, ACCESS_TIME=access_time)
        db_session = SessionMaker()
        db_session.add(new_session)
        db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        put_info('[create_session]'+'is failed')
        return False
    finally:
        db_session.close()
    return True


# Session Get
async def get_session_detail(session_id = None):
    if session_id is None:
        put_info('[get_session_detail]'+'session_id is not set')
        return False

    if isinstance(session_id, UUID):
        session_id = str(session_id)

    try:
        # Get seesion data
        db_session = SessionMaker()
        response = db_session.query(Session).filter(Session.SESSION_ID == session_id).first()
    except SQLAlchemyError as e:
        return False
    finally:
        db_session.close()
    return response


# Session Update
async def update_session(session_id = None, new_session_data = None) -> bool:
    if session_id is None:
        put_info('[update_session]'+'session_id is not set')
        return False

    if isinstance(session_id, UUID):
        session_id = str(session_id)

    if new_session_data is None:
        put_info('[update_session]'+'key is not set')
        return False

    try:
        db_session = SessionMaker()
        stored_session = db_session.query(Session).filter(Session.SESSION_ID == session_id).first()

        # Update session data
        if stored_session:
            new_session_data = await encrypt_data(new_session_data)
            stored_session.SESSION_DATA = new_session_data
            stored_session.ACCESS_TIME = datetime.now()
            db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        put_info('[update_session]'+'is failed')
        return False
    finally:
        db_session.close()
    return True


# Session Delete
async def delete_session(session_id = None) -> bool:
    if session_id is None:
        put_info('[delete_session]'+'session_id is not set')
        return False

    if isinstance(session_id, UUID):
        session_id = str(session_id)

    try:
        db_session = SessionMaker()
        stored_session = db_session.query(Session).filter(Session.SESSION_ID == session_id).first()

        # Delete session data
        if stored_session:
            db_session.delete(stored_session)
            db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        put_info('[delete_session]'+'is failed')
        return False
    finally:
        db_session.close()
    return True


# Session destruction
async def destroy(session_id: UUID = None) -> bool:
    if session_id is None:
        put_info('[destroy]'+'session_id is not set')
        return False

    # await backend.delete(session_id)
    await delete_session(session_id)
    return True


# Get Session All Data
async def getAll(session_id: UUID = None) -> dict:
    if session_id is None:
        put_info('[getAll]'+'session_id is not set')
        return False

    data = await get_session_detail(session_id)

    if data is None:
        put_info('[getAll]'+'session data is not found')
        return False
    else:
        # Decrypt Json session data
        get_data =  json.loads(await decrypt_data(data.SESSION_DATA))

        # Update access time
        await setTime(session_id)
    return get_data


# Get Session Variables
async def getVar(session_id: UUID = None, key: str = None) -> str:
    if session_id is None:
        put_info('[getVal]'+'session_id is not set')
        return False

    if key is None:
        put_info('[getVal]'+'key is not set')
        return False

    data = await get_session_detail(session_id)

    if data is None:
        put_info('[getVal]'+'session data is not found')
        return False
    else:
        # Decrypt Json session data
        session_data = json.loads(await decrypt_data(data.SESSION_DATA))
        get_data = session_data.get(key)

        # Update access time
        await setTime(session_id)
    return get_data


# Set Session Variables
async def setVar(session_id: UUID = None, key: str = None, val: str = None) -> bool:
    if session_id is None:
        put_info('[setVal]'+'session_id is not set')
        return False

    if key is None:
        put_info('[setVal]'+'key is not set')
        return False

    current_time = time.time()
    data = await get_session_detail(session_id)

    if data is None:
        put_info('[setVal]' + 'session data is not found')
        return False

    # Set key and value to session data
    get_data = json.loads(await decrypt_data(data.SESSION_DATA))
    get_data.update({key: val})
    update_data = json.dumps(get_data, ensure_ascii=False)

    # Update session data with key value
    respoonse = await update_session(session_id, update_data)
    return respoonse


# Delete Session Variables
async def unsetVar(session_id: UUID = None, key: str = None) -> bool:

    if session_id is None:
        put_info('[unsetVal]'+'session_id is not set')
        return False

    if key is None:
        put_info('[unsetVal]'+'key is not set')
        return False

    current_time = time.time()
    data = await get_session_detail(session_id)

    if data is None:
        put_info('[unsetVal]'+'session data is not found')
        return False

    # Unset key and value of session data
    get_data = json.loads(await decrypt_data(data.SESSION_DATA))
    del get_data[key]
    update_data = json.dumps(get_data)

    # Update session data with key value
    respoonse = await update_session(session_id, update_data)
    return respoonse


# Check for the existence of Session Variables
async def issetVar(session_id: UUID = None, key: str = None) -> bool:
    if session_id is None:
        put_info('[issetVal]'+'session_id is not set')
        return False

    if key is None:
        put_info('[issetVal]'+'key is not set')
        return False

    data = await get_session_detail(session_id)

    if data is None:
        put_info('[issetVal]'+'session data is not found')
        return False
    else:
        # Decrypt Json session data
        get_data = json.loads(await decrypt_data(data.SESSION_DATA))
        if key not in get_data:
            return False

        # Update access time
        await setTime(session_id)
    return True


# Get Session Time
async def getTime(session_id: UUID = None):
    if session_id is None:
        put_info('[getTime]'+'session_id is not set')
        return False

    data = await get_session_detail(session_id)

    if data is None:
        put_info('[getTime]'+'session data is not found')
        return False
    else:
        access_time = data.ACCESS_TIME
        get_time = int(access_time.timestamp())
    return get_time


# Set Session Time
async def setTime(session_id: UUID = None):
    if session_id is None:
        put_info('[setTime]'+'session_id is not set')
        return False

    data = await get_session_detail(session_id)

    if data is None:
        put_info('[setTime]'+'session data is not found')
        return False
    else:
        session_id = data.SESSION_ID

        # Decrypt Json session data
        get_data   = json.loads(await decrypt_data(data.SESSION_DATA))

        try:
            db_session = SessionMaker()
            stored_session = db_session.query(Session).filter(Session.SESSION_ID == session_id).first()

            # Update session accesstime
            if stored_session:
                stored_session.ACCESS_TIME  = datetime.now()
                db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            put_info('[setTime]'+'is failed')
            return False
        finally:
            db_session.close()
    return True


# Session timeout check
async def isValidTime(session_id: UUID = None) -> bool:
    if session_id is None:
        put_info('[isValidTime]'+'session_id is not set')
        return False

    current_time = time.time()
    access_time = await getTime(session_id)

    if access_time is None:
        put_info('[isValidTime]'+'access time is not set')
        return False

    # Calculate the time difference
    inactive_time = current_time - access_time

    # Check Session expired
    if inactive_time > timeout:
        return False
    return True
