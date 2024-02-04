from rest_framework import generics, renderers
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import logout
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Plant,CheckMaterialHistory,Store,CheckMaterial
from .serializers import PlantSerializer, StoreSerializer, MaterialSerializer, CheckMaterialHistorySerializer
from django.db import transaction
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import render


def home(request):
    return render(request,'a.html')

class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({'message': 'Login successful'})
class LogoutView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})
class PlantDataView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [renderers.JSONRenderer]
    def get(self, request, plantid):
        try:
            plant = Plant.objects.get(plantid=plantid)
            serializer = PlantSerializer(plant)
            return Response(serializer.data)
        except Plant.DoesNotExist:
            return Response({"error": "Plant not found"}, status=404)

class AllPlants(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=Plant.objects.all()
    serializer_class =PlantSerializer
    renderer_classes = [renderers.JSONRenderer]

class PlantStoredLocations(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, plantid):
        try:
            plant = Plant.objects.get(plantid=plantid)
            stores = Store.objects.filter(plant=plant)
            serializer = StoreSerializer(stores, many=True)
            return Response(serializer.data)
        except Plant.DoesNotExist:
            return Response({"error": "Plant not found"}, status=404)
class MaterialDataView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, plantid, storedid):
        try:
            plant = Plant.objects.get(plantid=plantid)
            store = Store.objects.get(storedlocationtid=storedid, plant=plant)
            materials = CheckMaterial.objects.filter(plant=plant, store=store)
            serializer = MaterialSerializer(materials, many=True)
            return Response(serializer.data)
        except (Plant.DoesNotExist, Store.DoesNotExist):
            return Response({"error": "Plant or stored location not found"}, status=404)


def is_close(value1, value2, rel_tol=1e-09, abs_tol=0.0):
    value1_float = float(value1)
    value2_float = float(value2)
    return abs(value1_float - value2_float) <= max(rel_tol * max(abs(value1_float), abs(value2_float)), abs_tol)

class MaterialDetailByNumber(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, plantid, storedid, material_number):
        try:
            # Retrieve plant, store, and material based on the provided IDs
            plant = Plant.objects.get(plantid=plantid)
            store = Store.objects.get(storedlocationtid=storedid, plant=plant)
            material = CheckMaterial.objects.filter(
                plant=plant, store=store, material__material_number=material_number
            ).first()
            if material:
                serializer = MaterialSerializer(material)
                return Response(serializer.data)
            else:
                return Response({"error": "Material not found"}, status=404)
        except (Plant.DoesNotExist, Store.DoesNotExist):
            return Response({"error": "Plant or stored location not found"}, status=404)

    def post(self, request, plantid, storedid, material_number):
        try:
            # Retrieve plant, store, and material based on the provided IDs
            plant = Plant.objects.get(plantid=plantid)
            store = Store.objects.get(storedlocationtid=storedid, plant=plant)
            material = CheckMaterial.objects.filter(
                plant=plant, store=store, material__material_number=material_number
            ).first()
            if material:
                stock_qty_material = request.data.get('stock_qty_material')
                if stock_qty_material is not None:
                    stock_qty_material = Decimal(stock_qty_material)
                    if is_close(stock_qty_material, material.stock_qty_material):
                        return Response({"message": "Stock quantity is already the same as the previous value"})

                    if stock_qty_material <= material.qty_material:
                        # Using Django transaction to ensure atomicity of database operations
                        with transaction.atomic():
                            # Only update if the stock_qty_material is different from the previous value
                            if not is_close(stock_qty_material, material.stock_qty_material):
                                material.stock_qty_material = stock_qty_material
                                material.last_update_stock_qty = timezone.now()
                                material.save()

                                # Save history in CheckMaterialHistory
                                User = get_user_model()
                                user = User.objects.get(pk=request.user.pk)  # Assuming user is authenticated
                                history = CheckMaterialHistory(
                                    material=material.material,
                                    plant=material.plant,
                                    store=material.store,
                                    qty_material=material.qty_material,
                                    unit_of_measure=material.unit_of_measure,
                                    stock_qty_material=material.stock_qty_material,
                                    last_update_stock_qty=material.last_update_stock_qty,
                                    user=user,
                                )
                                history.save()

                        return Response({"message": "Stock quantity updated successfully"})
                    else:
                        raise ValidationError("Stock quantity cannot be greater than qty_material.")
                else:
                    return Response({"error": "Invalid request. Missing 'stock_qty_material' field in the form data."}, status=400)
            else:
                return Response({"error": "Material not found"}, status=404)
        except (Plant.DoesNotExist, Store.DoesNotExist):
            return Response({"error": "Plant or stored location not found"}, status=404)


class CheckMaterialHistoryList(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CheckMaterialHistorySerializer

    def get_queryset(self):
        plantid = self.kwargs['plantid']
        storedid = self.kwargs['storedid']
        plant = get_object_or_404(Plant, plantid=plantid)
        store = get_object_or_404(Store, storedlocationtid=storedid, plant=plant)
        return CheckMaterialHistory.objects.filter(plant=plant, store=store)