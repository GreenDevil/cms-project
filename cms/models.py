import datetime
from django.contrib import admin
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from markdown import markdown


VIEWABLE_STATUS = [3, 4]


class ViewableManager(models.Manager):
    def get_queryset(self):
        default_queryset = super(ViewableManager, self).get_queryset()
        return default_queryset.filter(status__in=VIEWABLE_STATUS)


class Category(models.Model):
    """Категоря содержимого"""
    label = models.CharField(blank=True, max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "категории"

    def __unicode__(self):
        return self.label


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('label',)}


admin.site.register(Category, CategoryAdmin)


class Story(models.Model):
    """Элемент информационного наполнения нашего сайта,
    обычно соответствует странице"""

    STATUS_CHOICES = (
        (1, "Требуются доработки"),
        (2, "Требуется подтверждение"),
        (3, "Опубликовано"),
        (4, "В архиве"),
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField()
    category = models.ForeignKey(Category)
    markdown_content = models.TextField()
    html_content = models.TextField(editable=False)
    owner = models.ForeignKey(User)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ['modified']
        verbose_name_plural = "статьи"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.html_content = markdown(self.markdown_content)
        self.modified = datetime.datetime.now()
        super(Story, self).save()

    admin_object = models.Manager()
    object = ViewableManager()

    @permalink
    def get_absolute_url(self):
        return "cms-story", (), {'slug': self.slug}


class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created', 'modified')
    search_fields = ('title', 'content')
#    list_filter = ('status', 'owner', 'created', 'modified')   как это сделать???
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Story, StoryAdmin)