from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse

from utils import get_loggedin_user

from src.config.db import db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get('/dashboard')
def dashboard(request: Request):
    user = get_loggedin_user(request)
    if user:
        result = db.table('travel_plans').select('*').eq('user_id', user.id).execute()
        print(result.data)
        return templates.TemplateResponse('dashboard.html', {'request': request, 'plans': result.data})
    return RedirectResponse('/login')


