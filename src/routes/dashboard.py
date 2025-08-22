from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse

from utils import get_loggedin_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get('/dashboard')
def dashboard(request: Request):
    user = get_loggedin_user(request)
    if user:
        return templates.TemplateResponse('dashboard.html', {'request': request})
    return RedirectResponse('/login')


