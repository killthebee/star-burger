from django.db import models

class Banner(models.Model):
    slug = models.CharField('Слаг', max_length=40)
    image = models.ImageField('Файл картинки', upload_to='banners/')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.slug
