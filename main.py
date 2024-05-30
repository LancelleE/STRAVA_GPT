import requests
from flask import Flask, request, redirect
import threading
from dotenv import dotenv_values

# ----------------- CONFIG -----------------
config = dotenv_values(".env")

CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
CLIENT_REFRESH_TOKEN = config["CLIENT_REFRESH_TOKEN"]
CLIENT_AUTHORIZATION = None

# ----------------- FLASK -----------------
app = Flask(__name__)
