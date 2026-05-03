from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
    ]

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    color = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Admin response
    admin_comment = models.TextField(blank=True)
    commented_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='review_comments'
    )
    commented_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.customer_name} — {self.title}"
