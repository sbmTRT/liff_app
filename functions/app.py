from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from environs import Env
from fastapi import FastAPI, Depends, Cookie

from utils.session_utils import *
# from utils.user_utils import *
from utils.log_utils import *

app = FastAPI()
env = Env()
env.read_env()

@app.post("/start")
async def start_ses():
    try:
        sid = await session_start()
        if sid is None:
            raise Exception("Session start failed")

        # #initial session setup
        await setVar(sid, 'USERID', env('USERID'))                      #ログインユーザーID
        await setVar(sid, 'ROLE', env('ROLE'))                          #ログインユーザーの権限
        await setVar(sid, 'USER_NAME', env('USER_NAME'))                #ログインユーザー名
        await setVar(sid, 'USER_EMAIL', env('USER_EMAIL'))              #ログインユーザーのMailアドレス
        await setVar(sid, 'AUTH_FLAG', env('AUTH_FLAG'))                #ログインユーザーのAuth_flag

        # Set sid into cookie in JSON Response
        response = JSONResponse(content="Cookie is set successfully")
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
        return response


@app.get("/getAll")
async def get_all(sid: str = Cookie(default=None)):
    try:
        if sid is None:
            raise Exception("Session is expired")

        # Check valid session
        chkSes = await isValidTime(sid)
        if not chkSes:
            raise Exception("Session is expired")

        # Set sid into cookie in JSON Response
        data = await getAll(sid)
        response = JSONResponse(content=data)
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)

        return response

@app.post("/setVar")
async def set_var(key: str, value: str, sid: str = Cookie(default=None)):
    try:
        if sid is None:
            raise Exception("Session is expired")

        # Check valid session
        chkSes = await isValidTime(sid)
        if not chkSes:
            raise Exception("Session is expired")

        data = await setVar(sid,key,value)
        if data:
            msg = "Session value is set"
        else:
            msg = "Session value is not set"

        # Set sid into cookie in JSON Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
        return response

@app.get("/issetVar")
async def isset_var(key: str, sid: str = Cookie(default=None)):
    try:
        if sid is None:
            raise Exception("Session is expired")

        # Check valid session
        chkSes = await isValidTime(sid)
        if not chkSes:
            raise Exception("Session is expired")

        data = await issetVar(sid,key)
        if data:
            msg = "Session value exists in database"
        else:
            msg = "Session value doesn't exist in database"

        # Set sid into cookie in JSON Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
        return response

@app.get("/getVar")
async def get_var(key: str, sid: str = Cookie(default=None)):
    try:
        if sid is None:
            raise Exception("Session is expired")

        # Check valid session
        chkSes = await isValidTime(sid)
        if not chkSes:
            raise Exception("Session is expired")

        # Set sid into cookie in JSON Response
        data = await getVar(sid,key)
        response = JSONResponse(content=data)
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
        return response

@app.post("/unsetVar")
async def unset_var(key: str, sid: str = Cookie(default=None)):
    try:
        if sid is None:
            raise Exception("Session is expired")

        # Check valid session
        chkSes = await isValidTime(sid)
        if not chkSes:
            raise Exception("Session is expired")

        data = await unsetVar(sid,key)
        if data:
            msg = "Session value is removed"
        else:
            msg = "Session value is not removed"

        # Set sid into cookie in JSON Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
        return response

@app.get("/getTime")
async def get_time(sid: str = Cookie(default=None)):
    try:
        if sid is None:
            raise Exception("Session is expired")

        # Check valid session
        chkSes = await isValidTime(sid)
        if not chkSes:
            raise Exception("Session is expired")

        data = await getTime(sid)

        # Set sid into cookie in JSON Response
        response = JSONResponse(content=data)
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
        return response

@app.post("/setTime")
async def set_time(sid: str = Cookie(default=None)):
    try:
        if sid is None:
            raise Exception("Session is expired")

        # Check valid session
        chkSes = await isValidTime(sid)
        if not chkSes:
            raise Exception("Session is expired")

        data = await setTime(sid)
        if data:
            msg = "Session accesstime updated"
        else:
            msg = "Session accesstime is not updated"

        # Set sid into cookie in JSON Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
        return response

@app.get("/isValidTime")
async def valid_time(sid: str = Cookie(default=None)):
    try:
        if sid is None:
            raise Exception("Session is expired")

        # Check valid session
        data = await isValidTime(sid)
        if data:
            msg = "Session is valid"
        else:
            msg = "Session is expired"

        # Set sid into cookie in JSON Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=1800)
        return response

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
        return response

app.mount("/static", StaticFiles(directory="/mnt/c/fastapi_session/static"), name="static")
templates = Jinja2Templates(directory="templates")

user_data_list = [
    {
        "USERID": "900001167",
        "ROLE": "AA",
        "USER_NAME": "TESTER1",
        "USER_EMAIL": "tester1@signalbase.co.jp",
        "AUTH_FLAG": "A"
    },
    {
        "USERID": "900001167",
        "ROLE": "BB",
        "USER_NAME": "TESTER2",
        "USER_EMAIL": "tester2@signalbase.co.jp",
        "AUTH_FLAG": "B"
    },
    {
        "USERID": "900001167",
        "ROLE": "CC",
        "USER_NAME": "TESTER3",
        "USER_EMAIL": "tester3@signalbase.co.jp",
        "AUTH_FLAG": "C"
    },
    {
        "USERID": "900001167",
        "ROLE": "DD",
        "USER_NAME": "TESTER4",
        "USER_EMAIL": "tester4@signalbase.co.jp",
        "AUTH_FLAG": "D"
    },
    {
        "USERID": "900001167",
        "ROLE": "EE",
        "USER_NAME": "TESTER5",
        "USER_EMAIL": "tester5@signalbase.co.jp",
        "AUTH_FLAG": "E"
    },
    {
        "USERID": "A343HFg",
        "ROLE": "FF",
        "USER_NAME": "TESTER6",
        "USER_EMAIL": "tester6@signalbase.co.jp",
        "AUTH_FLAG": "F"
    },
    {
        "USERID": "S34df35",
        "ROLE": "FF",
        "USER_NAME": "TESTER6",
        "USER_EMAIL": "tester6@signalbase.co.jp",
        "AUTH_FLAG": "F"
    },
    {
        "USERID": "34dd3535",
        "ROLE": "FF",
        "USER_NAME": "TESTER6",
        "USER_EMAIL": "tester6@signalbase.co.jp",
        "AUTH_FLAG": "F"
    },
    {
        "USERID": "Eeerer3r",
        "ROLE": "FF",
        "USER_NAME": "TESTER6",
        "USER_EMAIL": "tester6@signalbase.co.jp",
        "AUTH_FLAG": "F"
    },
    {
        "USERID": "C212424",
        "ROLE": "FF",
        "USER_NAME": "TESTER6",
        "USER_EMAIL": "tester6@signalbase.co.jp",
        "AUTH_FLAG": "F"
    }
]

@app.get("/items_all", response_class=HTMLResponse)
async def read_item(request: Request, sid: str = Cookie(default=None)):
    try:
        return templates.TemplateResponse("user_info_all.html", {"request": request, "data": user_data_list})

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)

@app.get("/items_hidden", response_class=HTMLResponse)
async def read_item(request: Request, sid: str = Cookie(default=None)):
    try:
        return templates.TemplateResponse("user_info_hidden.html", {"request": request, "data": user_data_list})

    except Exception as err:
        msg = str(err)

        # Error Response
        response = JSONResponse(content=msg)
        response.set_cookie(key="sid", value=sid, max_age=0)
