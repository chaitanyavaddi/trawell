import json
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse
from src.integrations.openai import generate_plan
from utils import get_loggedin_user
from src.config.db import db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/plans/new')
def new_plan(request: Request):
    user = get_loggedin_user(request)
    if user:
        return templates.TemplateResponse('new_plan.html', {'request': request})
    return RedirectResponse('/login')


@router.post('/plans/new')
def create_plan(
   request: Request, 
   title: str = Form(...),
   days: int = Form(...),
   persons: int = Form(...),
   budget: str = Form(...),
   city: str = Form(...)
):
   user = get_loggedin_user(request)
   if user:
    result = db.table('travel_plans').insert({
       'user_id': user.id,
       'title': title,
       'days': days,
       'budget': budget,
       'cities': city,
       'persons_count': persons,
       'ai_plan': 'Nothing...'
    }).execute()

    if result.data:
       return RedirectResponse(f'http://127.0.0.1:8000/plans/generate?plan_id={result.data[0]["id"]}', status_code=302)

@router.get('/plans/generate')
def create_plan(request: Request, plan_id):
   print(plan_id)
   #1 Get record
   result = db.table('travel_plans').select('*').eq('id', plan_id).execute()
   
   if result.data:
    plan = generate_plan(str(result.data[0]))

    result1 = db.table('travel_plans').update({
        'ai_plan': plan
        }).eq('id', plan_id).execute()
    
    if result1.data:
       return JSONResponse(json.dumps(result1.data[0]))
    
   #2 Make GPT call to gerenate travel plan

   #3 Shoew HTML page prefilled with Plan