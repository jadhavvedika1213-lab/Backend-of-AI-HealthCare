from models.base import Document, now


class Prescription(Document):
    @classmethod
    def defaults(cls):
        return {"file_path": None, "doctor_name": None, "clinic_name": None, "date": now,
                "raw_text": None, "summary": None, "medicines": list}
