from fastapi import BackgroundTasks

def _send_email(to: str, subject: str, body: str):
    print(f"[BACKGROUND EMAIL] to={to} subject={subject} body={body}")

def appointment_confirmation(background_tasks: BackgroundTasks, to: str, appointment_number: str):
    background_tasks.add_task(_send_email, to, "Appointment Confirmation", f"Appointment {appointment_number} is confirmed.")

def appointment_reminder(background_tasks: BackgroundTasks, to: str, appointment_number: str):
    background_tasks.add_task(_send_email, to, "Appointment Reminder", f"Reminder for appointment {appointment_number}.")

def prescription_notification(background_tasks: BackgroundTasks, to: str, prescription_id: int):
    background_tasks.add_task(_send_email, to, "Prescription Created", f"Prescription #{prescription_id} has been created.")
