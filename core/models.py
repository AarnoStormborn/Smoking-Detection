from django.db import models

class FileUpload(models.Model):
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to="")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Alert(models.Model):
    file = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.file.name} => {str(self.timestamp)}"
    
