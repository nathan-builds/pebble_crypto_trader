from database.transaction import Transaction
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy_utils import database_exists, create_database
from database.transaction import Base
from testing.test_orders import TestOrderGenerator
from sqlalchemy.exc import SQLAlchemyError
import logging
from pebble_logger import PebbleLogger
import sys
from threading import Timer
import os


class DBWriter():
    def __init__(self):
        self.session = None
        self.create_connection()
        self.logger = self.get_logger()
        self.keep_connection_alive()

    def get_logger(self):
        p_log = PebbleLogger("DBWriter", True, True, 'logs/pebble_logs.log')
        logger = p_log.get_logger()
        return logger

    def create_connection(self):
        '''
        Establish a connection with the database. Create a new database if its the first startup and no database exists
        @return:
        '''
        try:
            engine = create_engine('mysql+pymysql://root:Password123@localhost:3333/pebble_live_v2', pool_pre_ping=True)
            if not database_exists(engine.url):
                create_database(engine.url)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            Base.metadata.create_all(engine)
        except SQLAlchemyError as e:
            self.log_database_error(e)

    def commit_to_db(self):
        '''
        Commits changes to the database
        @return:
        '''
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            self.log_database_error(e)

    def load_all_transactions(self):
        '''
        Get all existing transactions from the database
        @return:
        '''
        transactions = []
        try:
            transactions = self.session.query(Transaction).all()
        except SQLAlchemyError as e:
            self.session.rollback()
            self.log_database_error(e)

        return transactions

    def create_new_transaction(self, transaction):
        '''
        Creates a new transaction in the database
        @param transaction:
        @return:
        '''
        try:
            self.session.add(transaction)
            self.commit_to_db()
        except SQLAlchemyError as e:
            self.session.rollback()
            self.log_database_error(e)

    def update_transaction(self):
        '''
        Already have reference to the transaction object, just persist the changes to the DB
        @return:
        '''
        try:
            self.commit_to_db()
        except SQLAlchemyError as e:
            self.session.rollback()
            self.log_database_error(e)

    def keep_connection_alive(self):
        '''
        Every two hours query the database to keep the connection alive
        @return:
        '''
        try:
            self.session.query(Transaction).first()
            timer = Timer(7200, self.keep_connection_alive)
            timer.start()
        except SQLAlchemyError as e:
            self.session.rollback()
            self.log_database_error(e)

    def log_database_error(self, error):
        '''
        Immediately quit the program upon a database failure. This is protection against the creation of
        "orphan" orders if it were to keep going
        @param error: Database error message
        @return:
        '''
        self.logger.error(error)
        self.logger.error("SYSTEM SHUTTING DOWN")
        os._exit(-1)
