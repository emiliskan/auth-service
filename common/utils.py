import json
from datetime import datetime
from uuid import UUID


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (UUID, datetime)):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
