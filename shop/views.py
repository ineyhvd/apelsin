from typing import Optional
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, DetailView, DeleteView, ListView, UpdateView, FormView

from shop.models import Product, Category, Order, Comment
from shop.forms import OrderForm, ProductModelForm, CommentModelForm


class IndexView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'page_obj'
    paginate_by = 5

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        search_query = self.request.GET.get('q', '')
        filter_type = self.request.GET.get('filter', '')
        products = Product.objects.all()

        if category_id:
            products = products.filter(category_id=category_id)

        if filter_type == 'expensive':
            products = products.order_by('-price')[:5]
        elif filter_type == 'cheap':
            products = products.order_by('price')[:5]
        elif filter_type == 'rating':
            products = products.filter(rating__gte=4).order_by('-rating')

        if search_query:
            products = products.filter(name__icontains=search_query)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(product=self.object, is_negative=False)
        context['related_products'] = Product.objects.filter(category_id=self.object.category).exclude(
            id=self.object.id)
        return context


class OrderDetailView(DetailView, FormView):
    model = Product
    template_name = 'shop/detail.html'
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone_number = form.cleaned_data['phone_number']
            quantity = form.cleaned_data['quantity']

            if self.object.quantity >= quantity:
                self.object.quantity -= quantity
                self.object.save()

                Order.objects.create(
                    full_name=full_name,
                    phone_number=phone_number,
                    quantity=quantity,
                    product=self.object
                )

                messages.success(request, 'Order successfully sent')
            else:
                messages.error(request, 'Something went wrong...')

            return self.render_to_response(self.get_context_data(form=form))

        return self.render_to_response(self.get_context_data(form=form))


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'shop/create.html'
    success_url = reverse_lazy('shop:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create New'
        return context


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shop:products')


class ProductEditView(UpdateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'shop/create.html'

    def get_success_url(self):
        return reverse_lazy('shop:product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentModelForm
    template_name = 'shop/detail.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        form.instance.product = product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shop:product_detail', kwargs={'pk': self.kwargs['pk']})
