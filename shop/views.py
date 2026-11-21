from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Category, Product
from .forms import ProductFilterForm


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    form = ProductFilterForm(request.GET or None)
    category_slug = request.GET.get('category_slug')
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        ordering = form.cleaned_data.get('ordering')

        if q:
            products = products.filter(title__icontains=q)
        if category:
            products = products.filter(category=category)
            active_category = category
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)
        if ordering:
            products = products.order_by(ordering)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'form': form,
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'active_category': active_category,
        'no_results': not products.exists(),
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })
