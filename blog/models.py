from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to = "wiki/", blank=True, null=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:300]

class Comment(models.Model):
    blog_id = models.ForeignKey("Blog", on_delete=models.CASCADE, db_column="blog_id")
    comment_id=models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    writer = models.CharField(max_length=10)
    body = models.TextField()

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.TextField()