from django.shortcuts import get_object_or_404, render_to_response
from cms.models import Category, Story
from django.db.models import Q


def category(request, slug):
    """По заданному ключу категории отображается все элементы этой категории."""
    category = get_object_or_404(Category, slug=slug)
    story_list = Story.object.filter(category=category)
    heading = "Category: %s" % category.label
    return render_to_response("../cmsproject/../templates/story_list.html", locals())