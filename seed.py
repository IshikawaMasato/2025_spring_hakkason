# Make sure app is in your Python path
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(current_dir)

from models import db, Department, RegulationSubject, Teacher, Category, Account
from models import Subject, SubjectTeacher, Timetable, SubjectDay
from models import Review, Attendance, Todo, PreviousAttendance, RequiredUnit
from app import app  # Flaskアプリをインポート

from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()

# DB 初期化（必要に応じて）
# db.drop_all()
# db.create_all()

def seed():
    # Department
    departments = [Department(name=f"Department {i}", course_years=random.randint(2, 4)) for i in range(10)]
    db.session.add_all(departments)

    # RegulationSubject
    regulation_subjects = [RegulationSubject(name=f"Regulation Subject {i}") for i in range(10)]
    db.session.add_all(regulation_subjects)

    # Teacher
    teachers = [Teacher(name=fake.name()) for _ in range(10)]
    db.session.add_all(teachers)

    # Category
    categories = [Category(name=f"Category {i}") for i in range(10)]
    db.session.add_all(categories)

    db.session.commit()  # 外部キー制約のため一度コミット

    # Account
    accounts = [
        Account(
            name=fake.name(),
            email=fake.unique.email(),
            password_hash="hashed_password",
            salt="salt",
            grade=random.randint(1, 4),
            department_id=random.choice(departments).department_id
        ) for _ in range(10)
    ]
    db.session.add_all(accounts)

    # Subject
    subjects = [
        Subject(
            name=f"Subject {i}",
            credit=random.randint(1, 4),
            regulation_subject_id=random.choice(regulation_subjects).regulation_subject_id,
            semester=random.choice(["Spring", "Fall"]),
            teacher_id=random.choice(teachers).teacher_id,
            recommended_grade=random.randint(1, 4),
            category_id=random.choice(categories).category_id
        ) for i in range(10)
    ]
    db.session.add_all(subjects)

    db.session.commit()

    # SubjectTeacher
    subject_teachers = [
        SubjectTeacher(
            subject_id=random.choice(subjects).subject_id,
            teacher_id=random.choice(teachers).teacher_id
        ) for _ in range(10)
    ]
    db.session.add_all(subject_teachers)

    # Timetable
    timetables = [
        Timetable(
            account_id=random.choice(accounts).account_id,
            subject_id=random.choice(subjects).subject_id
        ) for _ in range(10)
    ]
    db.session.add_all(timetables)
    db.session.commit()

    # SubjectDay
    subject_days = [
        SubjectDay(
            subject_id=random.choice(subjects).subject_id,
            position=random.randint(1, 20)
        ) for _ in range(10)
    ]
    db.session.add_all(subject_days)

    # Review
    reviews = [
        Review(
            account_id=random.choice(accounts).account_id,
            subject_id=random.choice(subjects).subject_id,
            content=fake.paragraph(),
            difficulty=random.randint(1, 5),
            assignment=random.randint(1, 5),
            interest=random.randint(1, 5),
            speed=random.randint(1, 5),
            other=random.randint(1, 5)
        ) for _ in range(10)
    ]
    db.session.add_all(reviews)

    # Attendance
    attendances = [
        Attendance(
            timetable_id=random.choice(timetables).timetable_id,
            absent_date=fake.date_between(start_date='-30d', end_date='today')
        ) for _ in range(10)
    ]
    db.session.add_all(attendances)

    # Todo
    todos = [
        Todo(
            account_id=random.choice(accounts).account_id,
            content=fake.sentence(),
            deadline=fake.date_between(start_date='today', end_date='+30d')
        ) for _ in range(10)
    ]
    db.session.add_all(todos)

    # PreviousAttendance
    prevs = [
        PreviousAttendance(
            subject_id=random.choice(subjects).subject_id,
            grade=random.randint(1, 4),
            student_count=random.randint(10, 100)
        ) for _ in range(10)
    ]
    db.session.add_all(prevs)

    # RequiredUnit
    required_units = [
        RequiredUnit(
            department_id=random.choice(departments).department_id,
            grade=random.randint(1, 4),
            subject_id=random.choice(regulation_subjects).regulation_subject_id,
            required_units=random.randint(1, 20)
        ) for _ in range(10)
    ]
    db.session.add_all(required_units)

    db.session.commit()
    print("✅ Seeding completed!")

if __name__ == '__main__':
    # アプリケーションコンテキスト内で処理を実行
    with app.app_context():
        seed()
