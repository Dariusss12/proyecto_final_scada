from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import serial
import asyncio
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

DATABASE_URL = "sqlite:///./serial_data.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SERIAL_PORT = os.getenv("SERIAL_PORT")
BAUD_RATE = 9600

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    steam = Column(Float, nullable=False)
    movement = Column(Boolean, nullable=False)

Base.metadata.create_all(bind=engine)

def read_serial():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            line = ser.readline().decode("utf-8").strip()
            return line
    except serial.SerialException as e:
        print(f"Error reading serial port: {e}")
        return None

def save_to_db(steam: float, movement: bool):
    db = SessionLocal()
    try:
        new_entry = SensorData(steam=steam, movement=movement)
        db.add(new_entry)
        db.commit()
    finally:
        db.close()

async def send_email(subject: str, content: str):
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = EMAIL_RECIPIENT
    message["Subject"] = subject
    message.set_content(content)

    try:
        await aiosmtplib.send(
            message,
            hostname=EMAIL_HOST,
            port=EMAIL_PORT,
            start_tls=True,
            username=EMAIL_USER,
            password=EMAIL_PASS,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

async def periodic_serial_read():
    while True:
        data = read_serial()
        if data:
            try:
                parts = data.split(";")
                if len(parts) == 2:
                    steam = float(parts[0])
                    movement = bool(int(parts[1]))
                    save_to_db(steam, movement)
                    print(f"Data saved: steam={steam}, movement={movement}")
                    email_content = f"New Data Received:\nSteam: {steam}\nMovement: {movement}"
                    await send_email("New Sensor Data", email_content)
                else:
                    print(f"Invalid data format: {data}")
            except Exception as e:
                print(f"Error processing data: {e}")
        else:
            print("No data read from serial port.")
        await asyncio.sleep(30)

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(periodic_serial_read())
