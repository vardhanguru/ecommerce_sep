from .models import Category


def category_list(request):
    categories = list(Category.objects.order_by("name"))
    category_id = request.GET.get("category")
    selected_category = next(
        (category for category in categories if str(category.pk) == category_id),
        None,
    )
    return {
        "categories": categories,
        "selected_category": selected_category,
    }