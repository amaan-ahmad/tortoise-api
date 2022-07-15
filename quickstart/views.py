from quickstart.utils import get_error_body
from .serializers import CustomerGoalsSerializer, PlanCreateSerializer, UserSerializer, BrandSerializer, PlanSerializer, PromotionSerializer
from .models import Plan, Promotion, CustomerGoals, User, Brand
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import IntegrityError


class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class BrandsView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class PlansView(APIView):
    def get(self, request, brand_id=None):
        plans = None
        if(brand_id is not None):
            plans = Plan.objects.filter(brand_id=brand_id)
        else:
            plans = Plan.objects.all().select_related('brand')
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlanCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class PromotionsView(APIView):
    def get(self, request, plan_id):
        try:
            promotions = Promotion.objects.get(
                pk=plan_id).select_related('plan')
            serializer = PromotionSerializer(promotions, many=True)
            return Response(serializer.data)
        except Promotion.DoesNotExist:
            return Response(status=404)

    def post(self, request, plan_id):
        request.data['plan'] = plan_id
        try:
            # checks if the promotion already exists, if so, it deletes it and creates a new one
            # had to do this because the serializer does not allow the same plan_id again.
            Promotion.objects.filter(plan_id=plan_id).delete()
        except Promotion.DoesNotExist:
            pass
        serializer = PromotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class EnrollView(APIView):
    def post(self, request, plan_id):
        try:
            request.data['plan'] = plan_id
            plan_query = Plan.objects.get(pk=plan_id)
            plan = PlanSerializer(plan_query, many=False).data

            # * benefit_percentage is already handled by the serializer (increase if promotion applied)

            request.data['benefit_percentage'] = plan['benefit_percentage']
            request.data['benefit_type'] = plan['benefit_type']

            serializer = CustomerGoalsSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except (Plan.DoesNotExist, IntegrityError) as e:
            if(e.__class__.__name__ == 'IntegrityError'):
                return Response(data=get_error_body("Already Enrolled"), status=409)
            elif(e.__class__.__name__ == 'DoesNotExist'):
                return Response(data=get_error_body("Plan does not exists"), status=404)
            else:
                return Response(status=500)
