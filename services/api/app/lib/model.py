from tortoise.models import Model
from tortoise import fields


class Products(Model):

    id = fields.UUIDField(pk=True)
    name = fields.CharField(255)
    description = fields.TextField()

    def __str__(self):
        return self.id

    def output(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
        }


class Offers(Model):

    id = fields.CharField(255, pk=True)

    product = fields.ForeignKeyField(
        'model.Products', related_name='offers')

    price = fields.IntField(null=True)
    items_in_stock = fields.IntField(null=True)

    def __str__(self):
        return self.id

    def output(self) -> dict:
        return {
            "id": str(self.id),
            "product": str(self.product_id),
            "price": self.price,
            "items_in_stock": self.items_in_stock,
        }
