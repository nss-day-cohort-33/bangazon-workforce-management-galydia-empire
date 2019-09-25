from django.db import models
from django.urls import reverse

class TrainingProgram(models.Model):

    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()
    description = models.CharField(max_length=1000, blank=True)

    class Meta:
        verbose_name = ("TrainingProgram")
        verbose_name_plural = ("TrainingPrograms")

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("TrainingProgram_detail", kwargs={"pk": self.pk})