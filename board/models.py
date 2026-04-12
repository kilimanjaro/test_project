from django.db import models


class Post(models.Model):
    title = models.CharField(verbose_name="제목", max_length=200)
    content = models.TextField(verbose_name="내용")
    author = models.CharField(verbose_name="작성자", max_length=50)
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    views      = models.PositiveIntegerField(verbose_name="조회수", default=0)

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="게시글")
    author = models.CharField(verbose_name="작성자", max_length=50)
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.post.title} - {self.author}"
