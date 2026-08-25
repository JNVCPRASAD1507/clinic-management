def send_appointment_confirmation(
    patient_phone: str,
    appointment_number: str
):
    print(
        f"Appointment confirmation sent to {patient_phone} "
        f"for {appointment_number}"
    )


def send_appointment_reminder(
    patient_phone: str,
    appointment_number: str
):
    print(
        f"Appointment reminder sent to {patient_phone} "
        f"for {appointment_number}"
    )


def send_prescription_notification(
    patient_email: str,
    prescription_id: int
):
    print(
        f"Prescription notification sent to {patient_email} "
        f"for prescription {prescription_id}"
    )