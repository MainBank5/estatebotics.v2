from fastapi import FastAPI, APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from api.v1.chat import chat
from api.v1.onoffice import onoffice
from api.v1.properties import properties

# load environment variables
load_dotenv()


ORIGINS = ["*"]

# create app instance
app = FastAPI(
    title="Estatebotics",
    description="EstateBotics v2 is a real estate chatbot powered by FastAPI and the OnOffice API, designed to help users search and retrieve property listings through a conversational interface. The chatbot is integrated with OpenAI's GPT to provide an intuitive and seamless user experience.",
    version="2.0.0",
    redoc_url="/redoc",
    contact={
        "name": "Eliud",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,  # Allow these origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
    ],
    allow_headers=["*"],  # Allow all headers (Authentication, etc.)
)


# adding the endpoints to the base entry file
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(onoffice.router, prefix="/api/v1", tags=["on-office"])
app.include_router(properties.router, prefix="/ap1/v1", tags=["properties"])
