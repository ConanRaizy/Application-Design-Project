from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

from .models import Car, Review
from .forms import CarForm, ReviewForm, AdminCommentForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


# ─── AUTH ─────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'cars/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── DASHBOARD ROUTER ─────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    return redirect('admin_panel') if request.user.is_staff else redirect('showroom')


# ─── CUSTOMER VIEWS ───────────────────────────────────────────────────────────

@login_required
def showroom(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    cars = Car.objects.all().prefetch_related('reviews')
    return render(request, 'cars/showroom.html', {'cars': cars})


@login_required
def review_view(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('review_success')
    return render(request, 'cars/review_form.html', {'form': form})


@login_required
def review_success(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    return render(request, 'cars/review_success.html')


# ─── ADMIN VIEWS ──────────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    context = {
        'total_cars':      Car.objects.count(),
        'available_cars':  Car.objects.filter(status='available').count(),
        'sold_cars':       Car.objects.filter(status='sold').count(),
        'total_reviews':   Review.objects.count(),
        'pending_reviews': Review.objects.filter(is_approved=False).count(),
        'recent_cars':     Car.objects.order_by('-created_at')[:5],
        'recent_reviews':  Review.objects.order_by('-submitted_at')[:5],
    }
    return render(request, 'cars/admin_panel.html', context)


@login_required
@user_passes_test(is_admin)
def manage_cars(request):
    return render(request, 'cars/manage_cars.html', {'cars': Car.objects.all()})


@login_required
@user_passes_test(is_admin)
def add_car(request):
    form = CarForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vehicle added successfully.')
        return redirect('manage_cars')
    return render(request, 'cars/car_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_admin)
def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    form = CarForm(request.POST or None, instance=car)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vehicle updated successfully.')
        return redirect('manage_cars')
    return render(request, 'cars/car_form.html', {'form': form, 'action': 'Edit', 'car': car})


@login_required
@user_passes_test(is_admin)
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Vehicle deleted.')
        return redirect('manage_cars')
    return render(request, 'cars/confirm_delete.html', {'car': car})


@login_required
@user_passes_test(is_admin)
def manage_reviews(request):
    reviews = Review.objects.select_related('car', 'commented_by').all()
    return render(request, 'cars/manage_reviews.html', {'reviews': reviews})


@login_required
@user_passes_test(is_admin)
def add_comment(request, pk):
    review = get_object_or_404(Review, pk=pk)
    form = AdminCommentForm(request.POST or None, instance=review)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.commented_by = request.user
        obj.commented_at = timezone.now()
        obj.save()
        messages.success(request, 'Response saved.')
        return redirect('manage_reviews')
    return render(request, 'cars/add_comment.html', {'form': form, 'review': review})
