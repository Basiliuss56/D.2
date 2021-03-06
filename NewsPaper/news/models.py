from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, unique = True)
    author_raiting = models.IntegerField(default = 0)


    def update_raiting(self):
        posts = Post.objects.filter(author=self.id)
        post_raiting = sum([r.post_raiting * 3 for r in posts])
        comment_raiting = sum([r.comment_raiting for r in Comment.objects.filter(author=self.author)])
        all_to_post_comment_raiting = sum([r.comment_raiting for r in Comment.objects.filter(post__in = posts)])
        self.author_raiting = post_raiting + comment_raiting + all_to_post_comment_raiting
        self.save()




class Category(models.Model):
    name = models.CharField(max_length = 255, unique = True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'

    POST_TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    ]
    type = models.CharField(max_length=2, choices = POST_TYPES, default = NEWS)
    created_time = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory',)
    header = models.CharField(max_length = 255)
    article_text = models.TextField()
    post_raiting = models.IntegerField(default = 0)

    def preview(self):
        preview = self.article_text[:129] + '...'
        return preview

    def like(self):
        self.post_raiting += 1
        self.save()

    def dislike(self):
        self.post_raiting -= 1
        self.save()



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    comment_raiting = models.IntegerField(default = 0)

    def like(self):
        self.comment_raiting += 1
        self.save()

    def dislike(self):
        self.comment_raiting -= 1
        self.save()

