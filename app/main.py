from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Habit, Completion
from app.schemas import UserCreate, UserLogin, HabitCreate, HabitResponse, DashboardResponse
from app.auth import hash_password, verify_password, create_access_token
from datetime import date, timedelta
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBearer()


#DATABASE

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#AUTH HELPER

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


#AUTH ROUTES 

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token}


#HABIT ROUTES

@app.post("/habits", response_model=HabitResponse)
def create_habit(
    habit: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_habit = Habit(
        title=habit.title,
        description=habit.description,
        created_at=date.today(),
        user_id=current_user.id
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit


@app.get("/habits", response_model=list[HabitResponse])
def get_habits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Habit).filter(Habit.user_id == current_user.id).all()


@app.post("/habits/{habit_id}/complete")
def complete_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()

    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    today = date.today()

    existing = db.query(Completion).filter(
        Completion.habit_id == habit_id,
        Completion.date == today
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already completed today")

    completion = Completion(
        habit_id=habit_id,
        date=today
    )
    db.add(completion)
    db.commit()

    return {"message": "Habit marked as completed"}


#DASHBOARD

@app.get("/dashboard", response_model=DashboardResponse)
def dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()

    total_habits = len(habits)
    total_completions = 0

    for habit in habits:
        total_completions += db.query(Completion).filter(
            Completion.habit_id == habit.id
        ).count()

    # completion percentage (based on last 30 days)
    total_possible = total_habits * 30
    completion_percentage = (
        (total_completions / total_possible) * 100
        if total_possible > 0 else 0
    )

    # streak calculation
    streak = 0
    today = date.today()

    while True:
        check_date = today - timedelta(days=streak)
        completed_today = False

        for habit in habits:
            completion = db.query(Completion).filter(
                Completion.habit_id == habit.id,
                Completion.date == check_date
            ).first()

            if completion:
                completed_today = True
                break

        if completed_today:
            streak += 1
        else:
            break

    return {
        "total_habits": total_habits,
        "completion_percentage": round(completion_percentage, 2),
        "current_streak": streak
    }
@app.get("/")
def home():
    return {"message": "Habit Tracker API is running"}