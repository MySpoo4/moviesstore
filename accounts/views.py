from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList  # type: ignore
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from movies.models import SecurityQuestion
from django.contrib import messages


@login_required
def orders(request):
    template_data = {}
    template_data["title"] = "Orders"
    template_data["orders"] = request.user.order_set.all()
    return render(request, "accounts/orders.html", {"template_data": template_data})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home.index")


def login(request):
    template_data = {}
    template_data["title"] = "Login"
    if request.method == "GET":
        return render(request, "accounts/login.html", {"template_data": template_data})
    elif request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            template_data["error"] = "The username or password is incorrect."
            return render(
                request, "accounts/login.html", {"template_data": template_data}
            )
        else:
            auth_login(request, user)
            return redirect("home.index")


def signup(request):
    template_data = {}
    template_data["title"] = "Sign Up"
    if request.method == "GET":
        template_data["form"] = CustomUserCreationForm()
        return render(request, "accounts/signup.html", {"template_data": template_data})

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        if form.is_valid() and question and answer:
            user = form.save()
            SecurityQuestion.objects.create(user=user, question=question, answer=answer)
            return redirect("accounts.login")
        else:
            template_data["form"] = form
            template_data["error"] = (
                "Please fill all fields including security question and answer."
            )
            return render(
                request, "accounts/signup.html", {"template_data": template_data}
            )


def reset_password_security(request):
    template_data = {"title": "Reset Password"}
    if request.method == "POST":
        username = request.POST.get("username")
        answer = request.POST.get("answer")
        new_password = request.POST.get("new_password")
        try:
            user = User.objects.get(username=username)
            sq = SecurityQuestion.objects.get(user=user)
            if sq.check_answer(answer):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successful.")
                return redirect("accounts.login")
            else:
                template_data["error"] = "Incorrect answer."
        except (User.DoesNotExist, SecurityQuestion.DoesNotExist):
            template_data["error"] = "User or security question not found."
    return render(
        request,
        "accounts/reset_password_security.html",
        {"template_data": template_data},
    )


@login_required
def user_settings(request):
    template_data = {"title": "User Settings"}
    try:
        sq = SecurityQuestion.objects.get(user=request.user)
        template_data["question"] = sq.question
        template_data["answer"] = sq.answer
    except SecurityQuestion.DoesNotExist:
        sq = None

    if request.method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        if question and answer:
            if sq:
                sq.question = question
                sq.answer = answer
                sq.save()
            else:
                SecurityQuestion.objects.create(
                    user=request.user, question=question, answer=answer
                )
            template_data["success"] = "Security phrase updated."
            template_data["question"] = question
            template_data["answer"] = answer
        else:
            template_data["error"] = "Please fill both fields."
    return render(
        request, "accounts/user_settings.html", {"template_data": template_data}
    )
