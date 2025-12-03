from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    @property
    def devs(self):
        return list({freebie.dev for freebie in self.freebies})
    
    def give_freebie(self, dev, item_name, value, session):
        new_freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        session.add(new_freebie)
        session.commit()
        return new_freebie
    
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    @property
    def companies(self):
        return list({freebie.company for freebie in self.freebies})
    
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)
    
    def give_away(self, other_dev, freebie, session):
        if freebie in self.freebies:
            freebie.dev = other_dev
            session.add(freebie)
            session.commit()
            return True
        return False

    def __repr__(self):
        return f'<Dev {self.name}>'
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)

    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    dev_id = Column(Integer, ForeignKey('devs.id'), nullable=False)

    company = relationship('Company', backref=backref('freebies', cascade='all, delete-orphan'))
    dev = relationship('Dev', backref=backref('freebies', cascade='all, delete-orphan'))

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'

    def __repr__(self):
        return self.print_details()
