from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey,create_engine, MetaData
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

Base = declarative_base()



load_dotenv()
POSTGRE_URL = os.getenv('POSTGRE_URL')

class Game(Base):
    __tablename__ = 'games'
    id = Column(String, primary_key=True)
    date = Column(DateTime)
    day = Column(String)
    officials = relationship('Official', backref='game')
    player_stats = relationship('PlayerStats', backref='game')
    team_stats = relationship('TeamStats', backref='game')

class Official(Base):
    __tablename__ = 'officials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('games.id'))
    official_id = Column( Integer)
    first_name = Column(String)
    last_name = Column(String)
    jersey_num = Column(String)
    name = column_property(first_name + ' ' + last_name, deferred=True)

class PlayerStats(Base):
    __tablename__ = 'player_stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('games.id'))
    team_id = Column(Integer)
    team_abbreviation = Column(String)
    team_city = Column(String)
    player_id = Column(Integer)
    player_name = Column(String)
    nickname = Column(String)
    start_position = Column(String)
    comment = Column(String)
    minutes = Column(String)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    to = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Float)

class TeamStats(Base):
    __tablename__ = 'team_stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('games.id'))
    team_id = Column(Integer)
    team_name = Column(String)
    team_abbreviation = Column(String)
    team_city = Column(String)
    status = Column(String)
    minutes = Column(String)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    to = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Float)
    
class Cache(Base):
    __tablename__ = 'cache'
    user_query = Column(String(200), primary_key=True)
    sql_response = Column(String)



def create_tables(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)


