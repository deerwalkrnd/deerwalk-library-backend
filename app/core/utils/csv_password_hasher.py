from csv import DictReader
from typing import Any, Dict, List

from app.modules.auth.infra.services.argon2_hasher import Argon2PasswordHasher


async def csv_password_hasher(rows: DictReader[str]) -> List[Dict[str, Any]]:
    hasher = Argon2PasswordHasher()
    processed_csv:List[Dict[str, Any]] = []

    for row in rows:
        if not any(row.values()):
            continue

        if "password" in row and row["password"]:
            row["password"] = await hasher.hash_password(password=row["password"])
        
        processed_csv.append(row)

    return processed_csv
    
