from fastapi import FastAPI
from src.routes.excel import router as excel_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="SheetGen")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://sheetgen-frontend.vercel.app/"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
app.include_router(excel_router)