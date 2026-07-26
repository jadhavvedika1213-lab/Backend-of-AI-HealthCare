from models.base import Document


class Medicine(Document):
    @classmethod
    def defaults(cls):
        return {"dosage": None, "frequency": None, "duration": None, "instructions": None}
