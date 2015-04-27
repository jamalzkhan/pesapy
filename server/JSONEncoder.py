import json as _json
import json
from bson.objectid import ObjectId

class JSONEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, ObjectId):
      return str(o)
    return _json.JSONEncoder.default(self, o)
