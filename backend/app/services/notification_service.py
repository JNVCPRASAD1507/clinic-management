def send_appointment_confirmation(patient_phone: str, appointment_number: str) -> None:
    print(f"Appointment confirmation sent to {patient_phone} for {appointment_number}")


def send_appointment_reminder(patient_phone: str, appointment_number: str) -> None:
    print(f"Appointment reminder sent to {patient_phone} for {appointment_number}")


def send_prescription_notification(patient_phone: str, prescription_id: int) -> None:
    print(
        f"Prescription notification sent to {patient_phone} for prescription {prescription_id}"
    )
