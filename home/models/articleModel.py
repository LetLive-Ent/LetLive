from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.db import models
from home.models import Topic
from home.models import Author


def upload_location(instance, filename):
    """
    Upload location for article files.
    File will be uploaded to MEDIA_ROOT/article_images/article_<id>/<filename>
    """
    return '{0}/article_images/article_{1}/{2}'.format(
        settings.MEDIA_ROOT,
        instance.id,
        filename
    )

class ArticleManager(models.Manager):
    """
    Article objects manager.
    """
    def published(self, status=True):
        """
        Returns QuerySet of article objects and 
        filters the objects with the publish status.
        
        :param status: The filter for published status
        :type status: True or False
        """
        if status:
            return self.filter(
                published=True
            ).filter(publish_date_time__lte=timezone.now())

        # return non published articles
        return self.filter(published=False)

class Article(models.Model):
    #: The author of the article.
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    #: The topic which the article is about.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    #: The title of the article. It is the diaplayed article name.
    title = models.CharField(max_length=120)
    #: The article's content. It is a html content.
    content = models.TextField()
    #: Determines is the article is published or not.
    published = models.BooleanField(default=False)
    #: The published date.
    publish_date_time= models.DateTimeField(null=True)
    #: Timestamps.
    updated_date_time = models.DateTimeField(auto_now=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
    #: The cover image of the article.
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True
    )

    #: The article's objects manager.
    objects = ArticleManager()

    def save(self, *args, **kwargs):
        """
        Always set a publish date when publishing article.
        """
        if self.published == True and self.publish_date_time == None:
            self.publish_date_time = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date_time', 'updated_date_time']
        permissions = [
            ("publish_article", "Can publish an article"),
        ]

