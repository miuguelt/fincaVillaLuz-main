from app import db

class Vaccinations(db.Model):
    __tablename__ = "vaccinatios"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccines.id'), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    apprentice_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    animals = db.relationship('Animals', back_populates='vaccinations')
    vaccines = db.relationship('Vaccines', back_populates='vaccinations')
    apprentice = db.relationship('User', foreign_keys=[apprentice_id])
    instructor = db.relationship('User', foreign_keys=[instructor_id])

    def to_json(self):
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "vaccine_id": self.vaccine_id,
            "application_date": self.application_date.strftime('%Y-%m-%d'),
            "apprentice_id": self.apprentice_id,
            "instructor_id": self.instructor_id,
            "animals": self.animals.to_json(),
            "vaccines": self.vaccines.to_json(),
            "apprentice": self.apprentice.to_json(),
            "instructor": self.instructor.to_json()
        }
    

    