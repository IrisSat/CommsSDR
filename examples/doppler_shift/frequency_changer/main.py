"""
Main module for the frequency changer. This only calls upon the webserver
"""
from dotenv import load_dotenv
from frequency_changer_server import FrequencyChangerServer

if __name__ == '__main__':
    load_dotenv("../.env")
    FrequencyChangerServer()
