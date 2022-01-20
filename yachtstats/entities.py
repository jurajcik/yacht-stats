from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Boat(Base):
    __tablename__ = 'boat'

    id = Column(Integer, primary_key=True)
    boataround_ref = Column(String(255))
    title = Column(String(255))
    charter = Column(String(255))

    length = Column(Numeric(8, 2))
    year = Column(Integer)
    water_tank = Column(Integer)
    sail = Column(String(255))
    manufacturer = Column(String(255))
    model = Column(String(255))

    region = Column(String(255))
    city = Column(String(255))
    marina = Column(String(255))

    created_at = Column(DateTime(timezone=True))

    def __str__(self, *args, **kwargs):
        return 'Boat(id={}, ref={})'.format(self.id, self.boataround_ref)


class PricePoint(Base):
    __tablename__ = 'price_point'

    id = Column(Integer, primary_key=True)
    boat_id = Column(Integer, ForeignKey('boat.id'), nullable=False)
    base_price = Column(Numeric(8, 2))
    total_price = Column(Numeric(8, 2))
    discount = Column(Numeric(8, 2))
    created_at = Column(DateTime(timezone=True))
    rent_start = Column(Date)

    def __str__(self, *args, **kwargs):
        return 'PricePoint(boat_id={}, rent_start={}, collected_at={})'.format(self.boat_id, self.rent_start,
                                                                               self.collected_at)
