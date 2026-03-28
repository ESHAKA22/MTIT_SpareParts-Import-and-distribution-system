from bson import ObjectId

def serialize(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc