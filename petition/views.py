from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count

from petition.forms import PetitionForm
from petition.models import Petition


# Create your views here.
def index(request):
    petitions = Petition.objects.annotate(vote_count=Count("votes")).order_by(
        "-vote_count"
    )

    return render(request, "petition/index.html", {"petitions": petitions})


def show(request, id):
    petition = get_object_or_404(Petition, id=id)

    return render(request, "petition/show.html", {"petition": petition})


@login_required
def create(request):
    if request.method == "POST":
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)  # create object but don’t save yet
            petition.author = request.user  # set author manually
            petition.save()
            return redirect("petition.index")  # redirect after save
    else:
        form = PetitionForm()

    return render(request, "petition/create.html", {"form": form})


@login_required
def delete(request, id):
    petition = get_object_or_404(Petition, id=id, author=request.user.id)
    petition.delete()

    return redirect("petition.index")


@login_required
def vote(request, id):
    petition = get_object_or_404(Petition, id=id)
    user = request.user

    if petition.votes.filter(id=user.id).exists():
        petition.votes.remove(user)
    else:
        petition.votes.add(user)

    return redirect("petition.show", id=id)
