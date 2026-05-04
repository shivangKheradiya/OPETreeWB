"""
ConnectionFormModel

UI-only model for the connection form.
"""

from dataclasses import dataclass


@dataclass
class ConnectionFormModel:
    # -----------------------------
    # API / Project
    # -----------------------------
    api_url: str = "http://127.0.0.1:8000/"
    project_code: str = "XYZ"
    domain: str = "SKET"

    # -----------------------------
    # Local DB (UI only)
    # -----------------------------
    local_db_host: str = "localhost"
    local_db_port: str = "5433"
    local_db_name: str = "xyz"
    local_db_user: str = "postgres"
    local_db_password: str = "postgres"
