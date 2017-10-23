from __future__ import unicode_literals
from ..loginReg.models import User
from django.db import models

class QuoteManager(models.Manager):
    def validate(self, post):
        errors = {}

        for key, val in post.items():
            if len(val) < 1:
                errors[key] = '{} cannot be empty'.format(key.replace('_',' ').title())

        if 'message' not in errors and len(post['message']) < 10:
            errors['message'] = 'Quote message must be at least 10 characters'

        if 'author' not in errors and len(post['author']) < 3:
            errors['author'] = 'Author name must be at least 3 characters'
        return errors

    def add_quote(self, post, user_id):
        quote = self.create(
            message = post['message'],
            author = post['author'],
            poster = User.objects.get(id = user_id)
        )

    def favorite(self, quote_id, user_id):
        quote = Quote.objects.get(id = quote_id)
        user = User.objects.get(id = user_id)
        quote.likers.add(user)

    def unfavorite(self, quote_id, user_id):
        quote = Quote.objects.get(id = quote_id)
        user = User.objects.get(id = user_id)
        quote.likers.remove(user)

    def get_favorites(self, user_id):
        user = User.objects.get(id = user_id)
        allQuotes = self.all()
        return (allQuotes.filter(likers = user), allQuotes.exclude(likers = user))

    def get_posted(self, user_id):
        user = User.objects.get(id = user_id)
        postedQuotes = self.filter(poster = user)
        return (user, postedQuotes, postedQuotes.count())

class Quote(models.Model):
    message = models.TextField()
    author = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    poster = models.ForeignKey(User, related_name = 'posted_quotes')
    likers = models.ManyToManyField(User, related_name = 'liked_quotes')
    objects = QuoteManager()
    def __str__(self):
        return 'Quote:{}'.format(self.message)   
    def __repr__(self):
        return 'Quote:{}'.format(self.message)