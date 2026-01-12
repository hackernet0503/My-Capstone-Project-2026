from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import routes 
from app.models import models 

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LIFECARE API",
    description="Backend for the capstone project",
    version="1.0.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes.router, tags=["public"])


# start command = uvicorn app.main:app --reload

# git command after modifing or adding files and push to the branch

# git add .
# git commit -m"detail of code"
# git push

# to pull the changes

# git pull