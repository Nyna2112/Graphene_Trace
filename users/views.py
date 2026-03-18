from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BootstrapAuthenticationForm
from .models import User
from dashboard.models import ActivityLog


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:role_redirect')

    form = BootstrapAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        ActivityLog.objects.create(user=user, action='Login', details=f'{user.username} logged in')
        return redirect('dashboard:role_redirect')

    if request.method == 'POST' and not form.is_valid():
        messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    ActivityLog.objects.create(user=request.user, action='Logout', details=f'{request.user.username} logged out')
    logout(request)
    return redirect('login')
