import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Neo4jConnection:
    def __init__(self):
        # Extract values from environment variables
        self._uri = os.getenv("NEO4J_URI")
        self._user = os.getenv("NEO4J_USER")
        self._password = os.getenv("NEO4J_PASSWORD")
        
        # Check if any of the environment variables are missing
        if not self._uri or not self._user or not self._password:
            raise ValueError("Missing required Neo4j connection details in the .env file")
        
        # Set up the Neo4j driver
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def get_session(self):
        return self._driver.session()

    def close(self):
        self._driver.close()

# Initialize the connection
neo4j_connection = Neo4jConnection()
