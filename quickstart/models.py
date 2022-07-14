from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from django.db import models


class Base(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    uuid = models.UUIDField(unique=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(Base):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.name


class BenefitTypes(models.TextChoices):
    CASHBACK = 'CB', _('Cashback')
    EV = 'EV', _('Extra Voucher')


class Brand(Base):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Brands'

    def __str__(self):
        return self.name


class Plan(Base):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(
        'Brand', on_delete=models.CASCADE, related_name='plans')
    amount_options = models.JSONField(default=list)
    benefit_percentage = models.FloatField()
    tenure_options = models.JSONField(default=list)
    benefit_type = models.CharField(
        max_length=100, choices=BenefitTypes.choices)

    class Meta:
        db_table = 'Plans'

    def __str__(self):
        return self.name


class Promotion(Base):
    name = models.CharField(max_length=100)
    plan = models.OneToOneField(
        'Plan', on_delete=models.CASCADE, related_name='promotions')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    users_limit = models.IntegerField(blank=True, null=True)
    discount = models.FloatField()

    class Meta:
        db_table = 'Promotions'

    def __str__(self):
        return self.name


class CustomerGoals(Base):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='goals')
    plan = models.ForeignKey(
        'Plan', on_delete=models.CASCADE, related_name='enrollments')
    selected_tenure = models.IntegerField()
    selected_amount = models.IntegerField()
    benefit_percentage = models.FloatField()
    benefit_type = models.CharField(
        max_length=100, choices=BenefitTypes.choices)
    deposited_amount = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CustomerGoals'
        constraints = [models.UniqueConstraint(
            fields=['plan', 'user'], name='unique_enrollment')]

    def __str__(self):
        return self.user.name + ' ' + self.plan.name
