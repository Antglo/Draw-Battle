# backend/app/core/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Player model
class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    xp = Column(Integer, default=0)
    
    # Relationship with game sessions
    game_sessions = relationship("GameSession", back_populates="player")

# GameSession model
class GameSession(Base):
    __tablename__ = 'game_sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey('players.id'))
    player2_id = Column(Integer, ForeignKey('players.id'))
    round_number = Column(Integer, default=1)
    winner_id = Column(Integer, ForeignKey('players.id'))
    
    # Relationship with players
    player1 = relationship("Player", foreign_keys=[player1_id])
    player2 = relationship("Player", foreign_keys=[player2_id])
    winner = relationship("Player", foreign_keys=[winner_id])
