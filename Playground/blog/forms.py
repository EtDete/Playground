from django import forms
 
from .models import Personnage, Lieu
 
class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Personnage
        fields = ('lieu',)
    


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Personnage
        fields = ['id_personnage','nom', 'prenom', 'pseudonyme','orientation','force_de_combat', 'etat', 'lieu','photo']

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Lieu
        fields = ['id_lieu','disponibilite','photo']