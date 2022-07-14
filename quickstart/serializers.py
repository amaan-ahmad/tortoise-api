from django.utils.timezone import now
import dateutil.parser as DP
from pytz import utc
from rest_framework import serializers
from .models import User, Brand, Plan, Promotion, CustomerGoals


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'id']


def is_promotion_valid(plan_id):
    try:
        promotion = Promotion.objects.get(plan=plan_id)
        if(promotion is not None):
            if(promotion.users_limit is not None):
                # checks if the promotion has reached the limit of users
                return CustomerGoals.objects.filter(plan=plan_id).count() < promotion.users_limit
            if(promotion.start_date is not None and promotion.end_date is not None):
                # checks if the promotion has not expired
                return promotion.start_date <= now() and promotion.end_date >= now()
            else:
                return False
    except Promotion.DoesNotExist:
        return False


class PlanSerializer(serializers.ModelSerializer):

    is_promoted = serializers.SerializerMethodField('get_promotions')

    benefit_percentage = serializers.SerializerMethodField(
        'get_benefit_percentage')

    def get_benefit_percentage(self, obj):
        try:
            promotion = Promotion.objects.get(plan=obj.id)
            if(is_promotion_valid(obj.id)):
                return obj.benefit_percentage + promotion.discount
            else:
                return obj.benefit_percentage
        except Promotion.DoesNotExist:
            return obj.benefit_percentage

    def get_promotions(self, obj):
        return is_promotion_valid(obj.id)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'amount_options',
                  'benefit_percentage', 'tenure_options', 'benefit_type', 'brand', 'is_promoted']


# This is a bad idea, because it is not DRY. But was a quick way to get the serializer working.
class PlanCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Plan.objects.create(**validated_data)

    class Meta:
        model = Plan
        fields = ['name', 'amount_options',
                  'benefit_percentage', 'tenure_options', 'benefit_type', 'brand']


class PromotionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Promotion.objects.create(**validated_data)

    class Meta:
        model = Promotion
        fields = ['id', 'name', 'plan', 'start_date',
                  'end_date', 'users_limit', 'discount']


class CustomerGoalsSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return CustomerGoals.objects.create(**validated_data)

    class Meta:
        model = CustomerGoals
        fields = ['id', 'selected_tenure', 'selected_amount',
                  'benefit_percentage', 'benefit_type', 'deposited_amount', 'start_date', 'plan', 'user']
