import os

# Configuration for Code-to-Play Protocol

# List of processes to kill instantly when not in reward mode
BLOCKLIST = [
    "Overwatch.exe",
    "Battle.net.exe",
    "Steam.exe",
    "EpicGamesLauncher.exe",
    "GenshinImpact.exe",
    "StarRail.exe",
    "Valorant.exe",
    "RiotClientServices.exe",
    "LeagueClient.exe"
]

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "state.json")

# Security
# In a real production environment, this should be hidden or derived from a system secret.
# For this local tool, a hardcoded salt prevents casual text editing.
SALT = "CodeToPlay_SecureHash_2026_Salt_v1"

# Reward Settings
REWARD_DURATION_MINUTES = 90
