from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """Class for Product instance

    The product class
    """
    product_id = models.IntegerField()
    description = models.TextField(
            max_length=1024,
            blank=True,
            null=True,
    )
    datetime = models.DateTimeField(
            db_index=True,
            )
    longitude = models.DecimalField(
            max_digits=15,
            decimal_places=10
    )
    latitude = models.DecimalField(
            max_digits=15,
            decimal_places=10
    )
    elevation = models.IntegerField()

    class Meta:
        verbose_name_plural = 'products'

    def __unicode__(self):
       return 'Product: %s %s ' % (str(self.product_id), str(self.datetime))
