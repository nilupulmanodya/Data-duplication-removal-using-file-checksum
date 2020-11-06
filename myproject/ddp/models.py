from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    r_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Files(models.Model):
    hash = models.TextField()
    path = models.TextField()


    def __str__(self):
        return str(self.hash)

class Shared(models.Model):
    shared_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    shared_to = models.ForeignKey(User, null=True, related_name='f_shared_to', on_delete=models.SET_NULL)
    s_title = models.CharField(max_length=100, null=True)
    s_hash = models.ForeignKey(Files, null=True, on_delete=models.SET_NULL)
    s_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.shared_by)

class Uploads(models.Model):
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    u_title = models.CharField(max_length=100, unique=True, null=True)
    u_hash = models.ForeignKey(Files,  null=True, on_delete=models.SET_NULL)
    u_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uploaded_by)

class temUploads(models.Model):
    title = models.CharField(max_length=100, null=True)
    tem_file = models.FileField(upload_to='upload')