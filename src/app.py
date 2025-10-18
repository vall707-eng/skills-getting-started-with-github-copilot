"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Agregar nuevas actividades
activities.update({
    "Fútbol": {
        "description": "Entrenamientos y partidos amistosos de fútbol 5.",
        "schedule": "Lunes y Miércoles 17:00-19:00",
        "participants": [],
        "max_participants": 20,
    },
    "Baloncesto": {
        "description": "Prácticas y torneos internos de baloncesto.",
        "schedule": "Martes y Jueves 18:00-20:00",
        "participants": [],
        "max_participants": 15,
    },
    "Pintura": {
        "description": "Taller de pintura (óleo y acuarela) para explorar técnicas básicas y avanzadas.",
        "schedule": "Miércoles 16:00-18:00",
        "participants": [],
        "max_participants": 12,
    },
    "Teatro": {
        "description": "Clases de interpretación, expresión corporal y montaje de obra corta.",
        "schedule": "Viernes 17:00-19:30",
        "participants": [],
        "max_participants": 18,
    },
    "Club de Ajedrez": {
        "description": "Sesiones y torneos para aprender y mejorar en ajedrez.",
        "schedule": "Sábados 10:00-12:00",
        "participants": [],
        "max_participants": 16,
    },
    "Robótica": {
        "description": "Proyectos prácticos de robótica y programación con retos mensuales.",
        "schedule": "Viernes 16:00-18:00",
        "participants": [],
        "max_participants": 14,
    },
})


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Prevent overbooking if max_participants is set
    max_p = activity.get("max_participants")
    if max_p is not None and len(activity["participants"]) >= max_p:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
