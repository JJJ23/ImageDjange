from django.db import models
import uuid
# Create your models here.
def user_portfolio_directory_path(instance, filename):
    return 'image-{0}/{1}'.format(instance.id, filename)

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=user_portfolio_directory_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)