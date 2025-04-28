from django.db import models
import uuid
import os
import hashlib

def file_upload_path(instance, filename):
    """Generate file path for new file upload"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=file_upload_path)
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=64, unique=True, blank=True, null=True)
    reference_to = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='duplicates'
    )  # Reference to an existing file

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.original_filename

    def save(self, *args, **kwargs):
        if self.file and not self.hash:
            # Calculate hash
            hasher = hashlib.sha256()
            for chunk in self.file.chunks():
                hasher.update(chunk)
            self.hash = hasher.hexdigest()

        # Automatically populate file metadata
        if self.file:
            self.original_filename = self.file.name
            self.file_type = self.file.file.content_type
            self.size = self.file.size

        super().save(*args, **kwargs)

    @staticmethod
    def calculate_storage_savings():
        total_saved = 0
        for file in File.objects.filter(reference_to__isnull=False):
            total_saved += file.size
        return total_saved
