from django.contrib import admin

from .models import Article


class ScopeInline(admin.TabularInline):
    model = Article.tags.through
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
