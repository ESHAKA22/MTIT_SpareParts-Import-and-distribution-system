from data_service import ProductMockDataService

class ProductService:
    def __init__(self):
        self.data_service = ProductMockDataService()

    def get_all(self):
        return self.data_service.get_all_products()

    def get_by_id(self, product_id: int):
        return self.data_service.get_product_by_id(product_id)

    def create(self, product_data):
        return self.data_service.add_product(product_data)

    def update(self, product_id: int, product_data):
        return self.data_service.update_product(product_id, product_data)

    def delete(self, product_id: int):
        return self.data_service.delete_product(product_id)