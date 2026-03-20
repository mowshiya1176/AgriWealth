from django.db import models
from django.conf import settings


class WasteCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='🌿')

    class Meta:
        verbose_name_plural = 'Waste Categories'

    def __str__(self):
        return self.name


class WasteItem(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
    ]
    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('ton', 'Tonnes'),
        ('liter', 'Litres'),
        ('bundle', 'Bundles'),
    ]

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waste_items')
    category = models.ForeignKey(WasteCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200)
    possible_products = models.TextField(help_text='e.g. Compost, Biofertilizer, Biogas')
    image = models.ImageField(upload_to='waste_items/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.farmer.username}"

    def get_possible_products_list(self):
        return [p.strip() for p in self.possible_products.split(',')]
