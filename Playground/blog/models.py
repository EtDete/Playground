from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Personnage(models.Model):
    id_personnage = models.CharField(max_length=100,primary_key=True)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    pseudonyme = models.CharField(max_length=50)
    ORIENTATION_CHOIX = [("Super-Héros","Super-héros"),("Super-Vilain","Super-vilain")]
    orientation = models.CharField(max_length=100,choices=ORIENTATION_CHOIX)
    force_de_combat = models.IntegerField(default=1,validators=[MaxValueValidator(100),MinValueValidator(1)])
    ETAT_CHOIX = [("Fatigué","Fatigué"),("Reposé","Reposé"),("Colérique","Colérique"),("Heureux","Heureux")]
    etat = models.CharField(max_length=100,choices=ETAT_CHOIX)
    origineStory = models.TextField(blank=True,null=True)
    lieu = models.ForeignKey('Lieu',on_delete=models.CASCADE)
    photo = models.CharField(max_length=200,blank=True)

    def __str__(self):
            return self.id_personnage

class Lieu(models.Model):
    id_lieu = models.CharField(max_length=100,primary_key=True)
    DISPONIBILITE_CHOIX = [("Libre","Libre"),("Occupé","Occupé")]
    disponibilite = models.CharField(max_length=100, choices = DISPONIBILITE_CHOIX)
    photo = models.CharField(max_length=2000)

    def __str__(self):
        return self.id_lieu