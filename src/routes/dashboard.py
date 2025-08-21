from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")

db = create_client('https://lkolxrovwsrrdltbhcvw.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxrb2x4cm92d3NycmRsdGJoY3Z3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU2MTIwNjAsImV4cCI6MjA3MTE4ODA2MH0.uTjpEIHK-U_9pxRK5DF7AFHCZH0soRZmaurlwXuMs7k')



def get_loggedin_user(request: Request):
    token = request.cookies.get('user_session')
    result = db.auth.get_user(token)
    if result:
        return result.user
    return None

@router.get('/dashboard')
def dashboard(request: Request):
    user = get_loggedin_user(request)
    if user:
        return templates.TemplateResponse('dashboard.html', {'request': request})
    return RedirectResponse('/login')


