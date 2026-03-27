from bson import ObjectId

def serialize(product):
    product["id"] = str(product["_id"])
    del product["_id"]
    return product