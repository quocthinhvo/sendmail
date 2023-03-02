from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List
import yaml
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str


class ConfigUpdateSchema(BaseModel):
    MODE: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool


@app.get("/")
async def root():
    return JSONResponse(status_code=200, content={"status": "OK"})


@app.get("/send_json")
async def send_json():
    try:
        with open('/etc/tsr_api/test.json', mode="r") as jsonfile:
            response = jsonfile.read()
            return response
    except:
        return JSONResponse(status_code=500, content={"status": "An error has been encountered"})


@app.post("/send_mail")
async def send_mail(email: EmailSchema):
    try:
        # read config form yaml
        with open("config.yaml", "r") as yamlfile:
            configData = yaml.load(yamlfile, Loader=yaml.FullLoader)
            yamlfile.close()
        conf = ConnectionConfig(
            MAIL_USERNAME=configData["MAIL_USERNAME"],
            MAIL_PASSWORD=configData["MAIL_PASSWORD"],
            MAIL_FROM=configData["MAIL_FROM"],
            MAIL_PORT=configData["MAIL_PORT"],
            MAIL_SERVER=configData["MAIL_SERVER"],
            MAIL_STARTTLS=configData["MAIL_STARTTLS"],
            MAIL_SSL_TLS=configData["MAIL_SSL_TLS"],
            USE_CREDENTIALS=configData["USE_CREDENTIALS"],
            VALIDATE_CERTS=configData["VALIDATE_CERTS"]
        )
        message = MessageSchema(
            subject=email.dict().get("subject"),
            recipients=email.dict().get("email"),
            body=email.dict().get("body"),
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"status": "Send complete"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"status": "An exception occurred"})


@app.post("/config/update")
async def config_update(newconfigschema: ConfigUpdateSchema):
    newconfig = {
        'MODE': newconfigschema.dict().get("MODE"),
        'MAIL_USERNAME': newconfigschema.dict().get("MAIL_USERNAME"),
        'MAIL_PASSWORD': newconfigschema.dict().get("MAIL_PASSWORD"),
        'MAIL_FROM': newconfigschema.dict().get("MAIL_FROM"),
        'MAIL_PORT': newconfigschema.dict().get("MAIL_PORT"),
        'MAIL_SERVER': newconfigschema.dict().get("MAIL_SERVER"),
        'MAIL_STARTTLS': newconfigschema.dict().get("MAIL_STARTTLS"),
        'MAIL_SSL_TLS': newconfigschema.dict().get("MAIL_SSL_TLS"),
        'USE_CREDENTIALS': newconfigschema.dict().get("USE_CREDENTIALS"),
        'VALIDATE_CERTS': newconfigschema.dict().get("VALIDATE_CERTS")
    }
    try:
        with open("config.yaml", "w") as yamlfile:
            yamlWrite = yaml.dump(newconfig, yamlfile)
            yamlfile.close()
            return JSONResponse(status_code=200, content={"status": "Config update complete"})
    except:
        return JSONResponse(status_code=500, content={"status": "An exception occurred"})


@app.get("/config/get")
async def config_get():
    with open("config.yaml", "r") as yamlfile:
        configData = yaml.load(yamlfile, Loader=yaml.FullLoader)
        yamlfile.close()
        configData["MAIL_PASSWORD"] = ""
    return JSONResponse(configData)
