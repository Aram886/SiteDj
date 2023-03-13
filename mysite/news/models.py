from django.db import models
from django.urls import reverse_lazy

# annotate - divide on groups with aggregates Count, MAX, MIN, Sum and for.
# Look at the database functions


class News(models.Model):
    title = models.CharField(max_length=120, verbose_name='Name')
    content = models.TextField(blank=True, verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Published date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Photo', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Published')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Category")
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse_lazy('view_news', kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'News'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=120, db_index=True)

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']
