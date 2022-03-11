from sqlalchemy import create_engine, Column, BigInteger, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import random

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


DB_HOST = 'postgres2'
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

engine = create_engine((f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"), echo=True)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def generate_id():
    return random.randint(10**10, 10**11-1)


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()

class Prize(Base):
    __tablename__ = 'prize'

    id = Column(BigInteger, primary_key=True)
    description = Column(String)
    promo_id = Column(BigInteger, ForeignKey('promo.id'))
    promo = relationship("Promo", back_populates="prizes")
    result = relationship("Result", back_populates="prize")

    def __init__(
        self, name, description
    ):
        self.id = generate_id()
        self.name = name
        self.description = description

class Participant(Base):
    __tablename__ = 'participant'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    promo_id = Column(BigInteger, ForeignKey('promo.id'))
    promo = relationship("Promo", back_populates="participants")

    def __init__(
        self, name
    ):
        self.id = generate_id()
        self.name = name



class Promo(Base):
    __tablename__ = 'promo'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    prizes = relationship("Prize")
    participants = relationship("Participant")


    def __init__(
        self, name, description
    ):
        self.id = generate_id()
        self.name = name
        if description:
            self.description = description


def add_promo_to_db(
    session,
    name, description
):
    c = Promo(
        name, description
    )
    session.add(c)
    session.commit()
    return c.id


def get_promos_dict_list(session):
    promos = session.query(Promo).all()
    ans = []
    for p in promos:
        ans.append({
            "id": p.id,
            "name": p.name,
            "description": p.description
        })
    return ans

def get_promo_by_id(session, id):
    promos = session.query(Promo).where(Promo.id == id).all()
    ans = []
    for p in promos:
        dikt = {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "prizes": [],
            "participants": []
        }
        for pr in p.prizes:
            dikt["prizes"].append({
                "id" : pr.id,
                "description": pr.desription,
            })
        for par in p.participants:
            dikt["participants"].append({
                "id": par.id,
                "name": par.name
            })
        ans.append(dikt)
    return ans[-1]

def edit_promo(session, id, name, desc):
    promos = session.query(Promo).where(Promo.id == id).all()
    promo = promos[0]
    promo.name = name
    promo.description = desc
    session.commit()

def delete_promo(session, id):
    session.query(Promo).filter(Promo.id == id).delete()
    session.commit()

def add_participant(session, id, name):
    promo = session.query(Promo).where(Promo.id == id).all()[0]
    participant = Participant(name)
    promo.participants.append(participant)
    session.commit()
    return participant.id

def delete_participant(session, id):
    session.query(Participant).filter(Participant.id == id).delete()
    session.commit()

def add_prize(session, id, descr):
    promo = session.query(Promo).where(Promo.id == id).all()[0]
    prize = Prize(descr)
    promo.prizes.append(prize)
    session.commit()
    return prize.id

def delete_prize(session, id):
    session.query(Prize).filter(Prize.id == id).delete()
    session.commit()

def can_ruffle(session, id):
    promo = session.query(Promo).where(Promo.id == id).all()[0]
    if len(promo.participants) == len(promo.prozes):
        return True
    return False

def ruffle(session, id):
    promo = session.query(Promo).where(Promo.id == id).all()[0]
    ans = []
    # can make it better
    for i in range(len(promo.prizes)):
        part = promo.participants[i]
        prize = promo.prixes[i]
        ans.append({
            "winner": {
                "id": part.id,
                "name": part.name
            },
            "prize": {
                "id": prize.id,
                "description": prize.description
            }
        })
    return ans