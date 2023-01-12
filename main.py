from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List
app = FastAPI()

class EmailSchema(BaseModel):
   email: List[EmailStr]
   subject: str
   body: str

conf = ConnectionConfig(
    MAIL_USERNAME ="",
    MAIL_PASSWORD = "",
    MAIL_FROM = "",
    MAIL_PORT = 587,
    MAIL_SERVER = "",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

@app.get("/")
async def root():
    return JSONResponse(status_code=200, content={"status": "OK"})

@app.post("/send_mail")
async def send_mail(email: EmailSchema):
    try:
        message = MessageSchema(
            subject=email.dict().get("subject"),
            recipients=email.dict().get("email"), 
            body=email.dict().get("body"),
            subtype="html"
            )
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"status": "Send complete"})
    except:
        return JSONResponse(status_code=500, content={"status": "An exception occurred"})