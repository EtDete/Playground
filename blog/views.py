from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Personnage, Lieu
from django.contrib import messages
import random
import time

def personnage_list(request):
    personnages = Personnage.objects.all()
    lieux = Lieu.objects.all()
    return render(request, "blog/personnage_list.html", {'personnages': personnages, 'lieux': lieux})
 
def post_detail(request, id_personnage):
    personnage = get_object_or_404(Personnage, id_personnage=id_personnage)
    lieu = personnage.lieu
    form=MoveForm()
    if request.method == "POST":
        ancien_lieu = get_object_or_404(Lieu, id_lieu=personnage.lieu.id_lieu)
        form = MoveForm(request.POST, instance=personnage)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Lieu, id_lieu=personnage.lieu.id_lieu)
            
            if nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_lieu=="Ville" and personnage.etat=='Reposé':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                if personnage.orientation == "Super-Vilain":
                    personnage.etat="Colérique"
                    personnage.save()
                    messages.add_message(request, messages.SUCCESS, f'{personnage.pseudonyme} met la pagaille en ville !')
                    lancer_combat(request,personnage,personnages=Personnage.objects.all())
                else:
                    personnage.etat="Heureux"
                    personnage.save()
                    messages.add_message(request, messages.SUCCESS, f'{personnage.pseudonyme} aide les gens de la ville !')
                    lancer_combat(request,personnage,personnages=Personnage.objects.all())
                #nouveau_lieu.disponibilite="occupe"
                #nouveau_lieu.save()
                #messages.add_message(request, messages.SUCCESS, f'{personnage.pseudonyme} est bien arrivé en ville !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_lieu==f'Salle de repos' and personnage.etat=='Fatigué':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                personnage.etat="Reposé"
                personnage.save()
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, f'{personnage.pseudonyme} se repose dans sa chambre de repos !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_lieu=="Centre d'entrainement" and personnage.etat=='Reposé':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                personnage.etat="Fatigué"
                a = random.randint(1,5)
                personnage.force_de_combat+= a
                personnage.save()
                nouveau_lieu.disponibilite = "Libre"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, f'{personnage.pseudonyme} s\'entraine au centre d\'entrainement ! Il gagne +{a} force de combat !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_lieu==f'Endroit calme de {personnage.pseudonyme}'and (personnage.etat=="Heureux" or personnage.etat=="Colérique"):
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                personnage.etat="Fatigué"
                personnage.save()
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, f'{personnage.pseudonyme} se remet de ses émotions dans un endroit calme...')
            elif nouveau_lieu==ancien_lieu:
                messages.add_message(request, messages.WARNING, f'{personnage.pseudonyme} est déjà à cet endroit.')
            else :
                print('message')
                messages.add_message(request, messages.ERROR, f'Désolé, vous ne pouvez pas déplacer {personnage.pseudonyme} à cet endroit.')
        return redirect('post_detail', id_personnage=id_personnage)
    else:
        form = MoveForm()
        return render(request,
                  "C:/Users/etien/OneDrive/Documents/Centrale/2A/Info_t2/Playground/blog/templates/blog/post_detail.html",
                  {'personnage': personnage, 'lieu': lieu, 'form': form})
    


from .forms import CharacterForm, PlaceForm

def add_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personnage_list')  # Redirige vers une vue affichant tous les personnages
    else:
        form = CharacterForm()

    return render(request, 'blog/add_character.html', {'form': form})

def add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personnage_list')  # Redirige vers une vue affichant tous les lieux
    else:
        form = PlaceForm()

    return render(request, 'blog/add_place.html', {'form': form})

def lancer_combat(request,personnage,personnages):
    list_combattant =[]
    for person in personnages:
        if person.orientation != personnage.orientation:
            list_combattant.append(person)
    if list_combattant==[]:
        messages.add_message(request, messages.ERROR, "Il n'y a pas d'adversaire !")
    else:
        combattant = random.choice(list_combattant)
        messages.add_message(request, messages.ERROR, f'Un combat est lancé entre {personnage.pseudonyme} et {combattant.pseudonyme} !')
        time.sleep(3)
        if combattant.force_de_combat>personnage.force_de_combat:
            nouveau_lieu = get_object_or_404(Lieu,id_lieu=f'Endroit calme de {personnage.pseudonyme}')
            nouveau_lieu.disponibilite = "Occupé"
            nouveau_lieu.save()
            personnage.lieu = nouveau_lieu
            personnage.etat="Fatigué"
            if personnage.force_de_combat >5:
                a=random.randint(1,5)
                personnage.force_de_combat -= a
            personnage.save()
            messages.add_message(request, messages.ERROR, f'{personnage.pseudonyme} a été battu par {combattant.pseudonyme} et va se remettre de son combat dans un endroit calme ! Il perds {a} de force de combat !')
        else:
            nouveau_lieu = get_object_or_404(Lieu,id_lieu=f'Endroit calme de {combattant.pseudonyme}')
            nouveau_lieu.disponibilite = "Occupé"
            nouveau_lieu.save()
            combattant.lieu = nouveau_lieu
            combattant.etat="Fatigué"
            if combattant.force_de_combat >5:
                a = random.randint(1,5)
                combattant.force_de_combat -= a
            combattant.save()
            messages.add_message(request, messages.ERROR, f'{combattant.pseudonyme} a été battu par {personnage.pseudonyme} et va se remettre de son combat dans un endroit calme ! Il perds {a} de force de combat !')
            