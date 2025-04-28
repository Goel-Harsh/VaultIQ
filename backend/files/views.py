from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
import hashlib
from .models import File
from .serializers import FileSerializer

# Create your views here.

class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.filter(reference_to__isnull=True)

    def create(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided in the request.'}, status=400)

        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate hash for the file
        hasher = hashlib.sha256()
        for chunk in file_obj.chunks():
            hasher.update(chunk)
        file_hash = hasher.hexdigest()

        # Check for duplicates
        duplicate_file = File.objects.filter(hash=file_hash).first()
        if duplicate_file:
            # Create a reference to the existing file
            new_file = File.objects.create(
                original_filename=file_obj.name,
                file_type=file_obj.content_type,
                size=file_obj.size,
                reference_to=duplicate_file,  # Reference the existing file
            )
            serializer = self.get_serializer(new_file)
            return Response(serializer.data, status=201)

        # Save the file if it's unique
        data = {
            'file': file_obj,
            'original_filename': file_obj.name,
            'file_type': file_obj.content_type,
            'size': file_obj.size,
            'hash': file_hash,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = super().get_queryset()
        original_filename = self.request.query_params.get('original_filename', None)
        file_type = self.request.query_params.get('file_type', None)
        size_min = self.request.query_params.get('size_min', None)
        size_max = self.request.query_params.get('size_max', None)
        upload_date = self.request.query_params.get('upload_date', None)

        # Filter by original filename (case-insensitive)
        if original_filename:
            queryset = queryset.filter(original_filename__icontains=original_filename)

        # Filter by file type (e.g., "application/pdf")
        if file_type:
            queryset = queryset.filter(file_type=file_type)

        # Filter by size range (convert size_min and size_max to integers)
        if size_min:
            queryset = queryset.filter(size__gte=int(size_min))
        if size_max:
            queryset = queryset.filter(size__lte=int(size_max))

        # Filter by upload date (exact date match)
        if upload_date:
            queryset = queryset.filter(uploaded_at__date=upload_date)

        return queryset

@api_view(['GET'])
def storage_savings(request):
    savings = File.calculate_storage_savings()
    return Response({'storage_savings': savings})
