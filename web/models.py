from . import db

# TEST PURPOSE
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Test {self.test}>"