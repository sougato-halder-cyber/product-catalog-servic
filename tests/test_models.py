"""Product model."""
from service import db


class DataValidationError(Exception):
    pass


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    price = db.Column(db.Float, nullable=False, default=0.0)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "availability": self.availability,
            "price": self.price,
        }

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.category = data["category"]
            self.availability = bool(data["availability"])
            self.price = float(data.get("price", 0.0))
        except (KeyError, TypeError, ValueError) as err:
            raise DataValidationError(f"Invalid product data: {err}")
        return self

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        return cls.query.get(product_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).all()

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category).all()

    @classmethod
    def find_by_availability(cls, availability):
        return cls.query.filter_by(availability=availability).all()
