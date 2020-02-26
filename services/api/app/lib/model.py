from tortoise.models import Model
from tortoise import fields


class TimestampMixin():
    createdAt = fields.DatetimeField(auto_now_add=True)
    updatedAt = fields.DatetimeField(auto_now=True)


class Keys(Model):

    id = fields.UUIDField(pk=True)
    hash = fields.CharField(32, unique=True)
    key = fields.TextField(null=True)

    def __str__(self):
        return str(self.id)

    def output(self) -> dict:
        return {
            "id": str(self.id),
            "hash": self.hash,
            "key": self.key,
        }


class Products(Model):

    id = fields.UUIDField(pk=True)
    name = fields.CharField(255)
    description = fields.TextField()

    def __str__(self):
        return str(self.id)

    def output(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
        }


class Offers(Model, TimestampMixin):

    id = fields.CharField(255, pk=True)

    product = fields.ForeignKeyField(
        'model.Products', related_name='offers')

    price = fields.IntField(null=True)
    items_in_stock = fields.IntField(null=True)

    def __str__(self):
        return str(self.id)

    def output(self) -> dict:
        return {
            "id": str(self.id),
            "product": str(self.product_id),
            "price": self.price,
            "items_in_stock": self.items_in_stock,
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat(),
        }
