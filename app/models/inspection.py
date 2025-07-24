from datetime import datetime, timezone

from app import db


class Inspection(db.Model):
    __tablename__ = "inspections"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), nullable=False)
    inspected_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    damage_report = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum("pending", "reviewed", "completed", name="inspection_status"),
        default="pending",
        nullable=False,
    )
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Inspection {self.id} - {self.vehicle_number}>"
