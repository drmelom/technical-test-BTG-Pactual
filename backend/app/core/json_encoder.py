import json
from decimal import Decimal
from datetime import datetime
from bson import ObjectId, Decimal128
from typing import Any


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for MongoDB and Pydantic compatibility"""
    
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, Decimal128):
            return str(o)
        elif isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
