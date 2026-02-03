from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.services.leetcode import fetch_leetcode_stats
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# --- SIMULATED REAL-TIME DB ---
# In a real app, use Redis. Here, we use memory.
page_views = {
    "hero": 1204,
    "projects": 850,
    "coding": 942,
    "experience": 300
}
current_active_users = 14 # Fake "live" count

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# --- PAGE FRAGMENTS (Full Section Swaps) ---

@app.get("/page/hero", response_class=HTMLResponse)
async def page_hero(request: Request):
    # Increment view
    page_views['hero'] += 1
    return templates.TemplateResponse("sections/hero.html", {
        "request": request,
        "views": page_views['hero'],
        "live": current_active_users + random.randint(-2, 5)
    })

@app.get("/page/coding", response_class=HTMLResponse)
async def page_coding(request: Request):
    # Fetch REAL LeetCode Data
    lc_stats = await fetch_leetcode_stats("akash_1512_")
    page_views['coding'] += 1
    
    return templates.TemplateResponse("sections/coding.html", {
        "request": request,
        "lc": lc_stats,
        "views": page_views['coding']
    })

@app.get("/page/projects", response_class=HTMLResponse)
async def page_projects(request: Request):
    page_views['projects'] += 1
    # Logic: If user views projects, recommend clients
    recommendation = "Check out my Client Work next!" 
    return templates.TemplateResponse("sections/projects.html", {
        "request": request,
        "recommendation": recommendation
    })

@app.get("/page/experience", response_class=HTMLResponse)
async def page_experience(request: Request):
    return templates.TemplateResponse("sections/experience.html", {"request": request})