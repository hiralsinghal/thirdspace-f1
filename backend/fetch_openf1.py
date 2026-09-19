import json, time, os, sys, urllib.request, urllib.error
BASE = "https://api.openf1.org/v1/"
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

ENDPOINTS = ["laps", "stints", "pit", "race_control", "weather", "drivers","session_resul"]