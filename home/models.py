from django.db import models

class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"
    
   