from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, engine

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone = Column(String)

    clients = relationship("Client", lazy='joined')
    
    def __repr__(self):
        return f'User id: {self.id}, name: {self.username}'
    

class Client(Base):
    __tablename__ = 'clients'
    
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)

    id = Column(Integer, primary_key=True)
    email = Column(String)
    register_date = Column(Date)
    firstname = Column(String)
    lastname = Column(String)
    phone_number = Column(String)
    date_of_birth = Column(Date)

    users = relationship("User", lazy='joined', viewonly=True)
    orders = relationship("Order", lazy='joined')
    
    def __repr__(self):
        return f'Client id: {self.id}, name: {self.firstname}, {self.lastname}'
    

class Order(Base):
    __tablename__ = 'orders'
    
    client_id = Column(Integer, ForeignKey(Client.id), nullable=False, index=True)

    email = Column(String)
    id = Column(Integer, primary_key=True)
    date_created = Column(Date)
    date_closed = Column(Date)
    title = Column(String)
    status = Column(String)
    amount = Column(Integer)
    tax = Column(Float)
    earned = Column(Float)
    currency = Column(String)
    manager = Column(String)
    partner_id = Column(String)
    utm_source = Column(String)
    utm_medium = Column(String)
    utm_campaign = Column(String)
    utm_content = Column(String)
    utm_term = Column(String)
    tags = Column(String)


    clients = relationship("Client", lazy='joined', viewonly=True)
    
    def __repr__(self):
        return f'Order id: {self.id}, name: {self.title}, amount: {self.amount}, status: {self.status}'
    


class Expens(Base):
    __tablename__ = 'expenses'
    
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)

    date = Column(Date, primary_key=True)
    spend = Column(String)
    currency = Column(String)
    
    def __repr__(self):
        return f'За {self.date} пользователь потратил {self.spend}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)