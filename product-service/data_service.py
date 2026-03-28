from database import product_collection
from bson import ObjectId


class ProductMockDataService:

    # 🔹 Get all products
    def get_all_products(self):
        products = []
        for product in product_collection.find():
            product["id"] = str(product["_id"])   # convert ObjectId → string
            del product["_id"]                  # remove MongoDB _id
            products.append(product)
        return products

    # 🔹 Get product by ID
    def get_product_by_id(self, product_id: str):
        try:
            product = product_collection.find_one({"_id": ObjectId(product_id)})
            if product:
                product["id"] = str(product["_id"])
                del product["_id"]
                return product
            return None
        except:
            return None

    # 🔹 Add product (FIXED)
    def add_product(self, product_data):
        product_dict = product_data.dict()

        # Insert into MongoDB
        result = product_collection.insert_one(product_dict)

        # 🔥 Retrieve inserted document
        new_product = product_collection.find_one({"_id": result.inserted_id})

        # 🔥 Convert ObjectId → string
        new_product["id"] = str(new_product["_id"])
        del new_product["_id"]

        return new_product

    # 🔹 Update product
    def update_product(self, product_id: str, product_data):
        try:
            update_data = product_data.dict(exclude_unset=True)

            result = product_collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": update_data}
            )

            if result.modified_count == 1:
                return self.get_product_by_id(product_id)

            return None
        except:
            return None

    # 🔹 Delete product
    def delete_product(self, product_id: str):
        try:
            result = product_collection.delete_one({"_id": ObjectId(product_id)})
            return result.deleted_count == 1
        except:
            return False
        