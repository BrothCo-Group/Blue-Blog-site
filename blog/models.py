from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Blog(models.Model):
    owner= models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, editable=False, related_name="blogs", related_query_name="blog")
    title= models.CharField(_("Title"), max_length=500)

    slug= models.SlugField(_("Slug"),max_length=500, editable=False)

class BlogPost(models.Model):
    blog= models.ForeignKey(Blog, verbose_name=_("Blog"), on_delete=models.CASCADE, related_name="posts", related_query_name="post")
    title= models.CharField(_("Title"), max_length=500)
    body= models.TextField(_("Body"))

    shared_to = models.ManyToManyField(Blog, verbose_name=_("Shared to"), related_name="shared_posts")

    is_published= models.BooleanField(_("Is published"), default=False)

    slug= models.SlugField(_("Slug"), max_length=500, editable=False)
