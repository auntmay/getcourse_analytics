from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, engine

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone = Column(Integer)

    clients = relationship("Clients", lazy='joined')
    
    def __repr__(self):
        return f'User id: {self.id}, name: {self.username}'
    

class Clients(Base):
    __tablename__ = 'clients'
    
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)

    client_id = Column(Integer, primary_key=True)
    email = Column(String)
    register_date = Column(Integer)
    firstname = Column(String)
    lastname = Column(String)
    phone_number = Column(Integer)
    date_of_birth = Column(Integer)

    users = relationship("User", lazy='joined', viewonly=True)
    orders = relationship("Orders", lazy='joined')
    
    def __repr__(self):
        return f'Client id: {self.client_id}, name: {self.firstname}, {self.lastname}'
    

class Orders(Base):
    __tablename__ = 'orders'
    
    client_id = Column(Integer, ForeignKey(Clients.client_id), nullable=False, index=True)

    order_id = Column(Integer, primary_key=True)
    date_created = Column(Integer)
    date_closed = Column(Integer)
    title = Column(String)
    status = Column(String)
    amount = Column(Integer)
    manager = Column(String)
    from_partner = Column(String)

    clients = relationship("Clients", lazy='joined', viewonly=True)
    
    def __repr__(self):
        return f'Order id: {self.order_id}, name: {self.title}, amount: {self.amount}, status: {self.status}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)