from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user     = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            next_url = request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect("core:home")

        messages.error(request, "Credenciais inválidas ou acesso não autorizado.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("core:home")