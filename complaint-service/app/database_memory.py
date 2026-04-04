# In-memory database for testing
from typing import List, Dict, Any
import uuid

class MemoryCollection:
    def __init__(self):
        self.data: List[Dict[str, Any]] = []
    
    def insert_one(self, document: Dict[str, Any]):
        document["_id"] = str(uuid.uuid4())
        self.data.append(document)
        result = type('Result', (), {'inserted_id': document["_id"]})()
        return result
    
    def find_one(self, query: Dict[str, Any]):
        for doc in self.data:
            match = True
            for key, value in query.items():
                if key == "_id":
                    if doc.get("_id") != value:
                        match = False
                        break
                elif doc.get(key) != value:
                    match = False
                    break
            if match:
                return doc
        return None
    
    def find(self, query: Dict[str, Any] = None):
        if query is None:
            return self.data
        
        results = []
        for doc in self.data:
            match = True
            for key, value in query.items():
                if doc.get(key) != value:
                    match = False
                    break
            if match:
                results.append(doc)
        return results
    
    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]):
        doc = self.find_one(query)
        if doc:
            doc.update(update.get("$set", {}))
            return type('Result', (), {'modified_count': 1})()
        return type('Result', (), {'modified_count': 0})()
    
    def delete_one(self, query: Dict[str, Any]):
        for i, doc in enumerate(self.data):
            match = True
            for key, value in query.items():
                if key == "_id":
                    if doc.get("_id") != value:
                        match = False
                        break
                elif doc.get(key) != value:
                    match = False
                    break
            if match:
                del self.data[i]
                return type('Result', (), {'deleted_count': 1})()
        return type('Result', (), {'deleted_count': 0})()
    
    def delete_many(self, query: Dict[str, Any]):
        to_delete = []
        for doc in self.data:
            match = True
            for key, value in query.items():
                if doc.get(key) != value:
                    match = False
                    break
            if match:
                to_delete.append(doc)
        
        for doc in to_delete:
            self.data.remove(doc)
        
        return type('Result', (), {'deleted_count': len(to_delete)})()

# Create memory collections
complaint_collection = MemoryCollection()
