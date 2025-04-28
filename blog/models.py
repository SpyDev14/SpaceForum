from django.utils import timezone
from django.conf  import settings
from django.db    import models

class Post(models.Model):
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete = models.CASCADE
	)

	title = models.CharField(max_length = 256)
	text  = models.TextField()

	published_date = models.DateTimeField(default = timezone.now)

	def publish(self) -> None:
		self.save()

	def __str__(self) -> str:
		return str(self.title)