from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag


class ScopeInlineFormset(BaseInlineFormSet):

    def clean(self):
        lst_tag = []
        count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_main', False):
                    count += 1
                if form.cleaned_data.get('tag') in lst_tag:
                    raise ValidationError('Нельзя выбрать один и тот же раздел два раза')
                else:
                    lst_tag.append(form.cleaned_data.get('tag'))
        if count == 0:
            raise ValidationError('Укажите основной раздел')
        elif count > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Article.tags.through
    formset = ScopeInlineFormset
    extra = 3


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
