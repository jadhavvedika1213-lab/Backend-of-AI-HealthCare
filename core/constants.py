class UserRole:
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"
    ALL = [ADMIN, DOCTOR, PATIENT]

class ReminderStatus:
    PENDING = "pending"
    COMPLETED = "completed"
    MISSED = "missed"
    ALL = [PENDING, COMPLETED, MISSED]

class MedicalDocCategory:
    LAB_REPORT = "lab_report"
    PRESCRIPTION = "prescription"
    X_RAY = "x_ray"
    MRI = "mri"
    CT_SCAN = "ct_scan"
    OTHER = "other"
    ALL = [LAB_REPORT, PRESCRIPTION, X_RAY, MRI, CT_SCAN, OTHER]

class ChatMessageRole:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ALL = [USER, ASSISTANT, SYSTEM]

class NotificationChannel:
    EMAIL = "email"
    SYSTEM = "system"
    WEBSOCKET = "websocket"
    ALL = [EMAIL, SYSTEM, WEBSOCKET]
