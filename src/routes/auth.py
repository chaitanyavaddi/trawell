from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")

db = create_client('https://lkolxrovwsrrdltbhcvw.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxrb2x4cm92d3NycmRsdGJoY3Z3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU2MTIwNjAsImV4cCI6MjA3MTE4ODA2MH0.uTjpEIHK-U_9pxRK5DF7AFHCZH0soRZmaurlwXuMs7k')


@router.get('/')
def home():
    return RedirectResponse('/signup')

@router.get('/signup')
def signup(request: Request):
    return templates.TemplateResponse("signup.html", { 'request': request})

@router.post('/api/signup')
def api_signup(request: Request, email = Form(...), password = Form(...)):
    result = db.auth.sign_up({
        'email': email,
        'password': password
    })

    if result.user:
        return JSONResponse({
            'message': 'User Created successfully',
            'token': result.session.access_token
        })

@router.get('/login')
def login(request: Request):
    return templates.TemplateResponse("login.html", { 'request': request})

@router.post('/api/login')
def api_login(request: Request, email = Form(...), password = Form(...)):
    result = db.auth.sign_in_with_password({
        'email': email,
        'password': password
    })

    if result.user:
        response =  RedirectResponse('/dashboard', status_code=302)
        response.set_cookie('user_session', result.session.access_token, max_age=3600)
        return response
        
