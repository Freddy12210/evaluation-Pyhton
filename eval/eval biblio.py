# Evaluation de la bibliotheque
class Bibliotheque():
    _instance = None
    def __init__(self, nom):
        if Bibliotheque._instance != None:
            raise Exception("Cette classe est un singleton")
        else:
            Bibliotheque._instance = self
            self.nom = nom
            self.livres = []
            self.utilisateurs = []
            self.json_file = 'bibliotheque.json'

    @classmethod
    def getInstance(self):
        if Bibliotheque._instance == None:
            Bibliotheque()
        return Bibliotheque._instance

    def action(self):
        choix = int(input("Que voulez vous faire ?\n1. Ajouter un livre\n2. Retirer un livre\n3. Afficher les livre\n4. Rechercher un livre\n5. Ajouter un utilisateur\n6. Afficher les utilisateur\n7. Emprunter un livre\n8. Rendre un livre\n9. Sauvegarder la bibliotheque\n10. Quitter\n"))
        match choix:
            case 1:
                #On ajoute un livre puis on retourne au menu
                self.ajoutLivre()
                self.action()
            case 2:
                #On retire un livre puis on retourne au menu
                self.retirerLivre()
                self.action()

            case 3:
                #afficher les livres puis une fois afficher on retourne au menu
                self.afficherLivre()
                self.action()
            case 4:
                #Rechercher un livre par titre, par auteur ou par catégorie.
                self.rechercherLivre()
                self.action()
            case 5:
                typeUtilisateur = int(input("Quel type d'utilisateur voulez vous ajouter ?\n1. Enfant\n2. Adulte\n"))
                match typeUtilisateur:
                    case 1:
                        self.ajouterUtilisateur('enfant')
                    case 2:
                        self.ajouterUtilisateur('adulte')
                self.action()
            case 6:
                #Afficher les utilisateurs puis une fois afficher on retourne au menu
                self.afficherUtilisateur()
                self.action()
            case 7:
                #Emprunter un livre
                self.emprunterLivre()
                self.action()
            case 8:
                #Rendre un livre
                self.rendreLivre()
                self.action()
            case 9:
                self.SauvegarderBibliotheque()
                self.action()
            case 10:
                print("Merci d'avoir visité notre bibliothèque !!\nAu revoir")
                exit()
            case _:
                print("Veuillez choisir un nombre entre 1 et 10")
                self.action()

    def afficheNom(self):
        print(self.nom)

    def ajoutLivre(self):
        #On demande les infos du livre
        typeLivre = int(input("Quel type de livre voulez vous ajouter ?\n1. BD\n2. Manga\n"))
        match typeLivre:
            case 1:
                print("Ajout d'une BD")
                newLivre = livresFactory().get_livre('bd', input("Titre : "), input("Auteur : "), input("Année : "), input("Catégorie : "), input("Illustrateur : "))
            case 2:
                print("Ajout d'un Manga")
                newLivre = livresFactory().get_livre('manga', input("Titre : "), input("Auteur : "), input("Année : "), input("Catégorie : "), input("Mangaka : "))
            case _:
                print("Veuillez entrer une valeur valide")
        self.livres.append(newLivre)
        print("Livre ajouté avec succès")

    def retirerLivre(self):
        #On demande les infos du livre
        titre = input("Titre du livre à retirer : ")
        for livre in self.livres:
            if livre.titre == titre:
                self.livres.remove(livre)
                print("Livre retiré avec succès")
                return
        print("Ce livre n'existe pas")

    def afficherLivre(self):
        #si la liste est vide on affiche un message
        if len(self.livres) == 0:
            print("Il n'y a pas de livres")
        else:
            print("Liste des livres :")
            for livre in self.livres:
                livre.afficheInfos()

    def rechercherLivre(self):
        typeRecherche = int(input("Comment voulez vous rechercher le livre ?\n1. Par titre\n2. Par auteur\n3. Par catégorie\n"))
        match typeRecherche:
            case 1:
                titre = input("Titre du livre à rechercher : ")
                for livre in self.livres:
                    if livre.titre == titre:
                        livre.afficheInfos()
                        return
                print("Ce livre n'existe pas")
            case 2:
                auteur = input("Auteur du livre à rechercher : ")
                for livre in self.livres:
                    if livre.auteur == auteur:
                        livre.afficheInfos()
                        return
                print("Ce livre n'existe pas")
            case 3:
                categorie = input("Catégorie du livre à rechercher : ")
                for livre in self.livres:
                    if livre.categorie == categorie:
                        livre.afficheInfos()
                        return
                print("Ce livre n'existe pas")
            case _:
                print("Veuillez entrer une valeur valide")

    def ajouterUtilisateur(self, type):
        #On demande les infos de l'utilisateur
        newUtilisateur = None
        if type == "enfant":
            print("Ajout d'un enfant")
            newUtilisateur = UtilisateurFactory().get_utilisateur(type, input("Nom : "), input("Prenom : "), input("Age : "), input("Ecole : "))
        elif type == "adulte":
            print("Ajout d'un adulte")
            newUtilisateur = UtilisateurFactory().get_utilisateur(type, input("Nom : "), input("Prenom : "), input("Age : "), input("Metier : "))
        else:
            print("Veuiller entrer une valeur valide")
        print("Utilisateur ajouté avec succès")
        self.utilisateurs.append(newUtilisateur)

    def afficherUtilisateur(self):
        #si la liste est vide on affiche un message
        if len(self.utilisateurs) == 0:
            print("Il n'y a pas d'utilisateurs")
        else:
            print("Liste des utilisateurs :")
            for utilisateur in self.utilisateurs:
                if utilisateur.__class__.__name__ == "Enfant":
                    utilisateur.afficherEnfant()
                elif utilisateur.__class__.__name__ == "Adulte":
                    utilisateur.afficherAdulte()

    def emprunterLivre(self):
        titre = input("Titre du livre à emprunter : ")
        for livre in self.livres:
            if livre.titre == titre:
                livre.disponible = False
                print("Livre emprunté avec succès")
                return
        print("Ce livre n'est pas dans la bibliothèque")

    def rendreLivre(self):
        titre = input("Titre du livre à rendre : ")
        for livre in self.livres:
            if livre.titre == titre and livre.disponible == False:
                livre.disponible = True
                print("Livre rendu avec succès")
                return
        print("Ce livre n'est pas dans la bibliothèque")

    def SauvegarderBibliotheque(self):
        #Sauvegarde de lʼétat : Sauvegarder lʼétat de la bibliothèque dans un fichier au format JSON.
        import json
        data = {
                "nom": self.nom,
                "utilisateurs": [utilisateur.__dict__ for utilisateur in self.utilisateurs],
                "livres": [livre.__dict__ for livre in self.livres]
            }
        with open('bibliotheque.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"L'état de la bibliothèque a été sauvegardé.")



class Livres:
    def __init__(self, titre, auteur, annee, categorie):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.categorie = categorie
        self.disponible = True
    
    def afficheInfos(self):
        print(f"Titre : {self.titre}\nAuteur : {self.auteur}\nAnnée : {self.annee}\nCatégorie : {self.categorie}\nDisponible : {self.disponible}")

class BD(Livres):
    def __init__(self, titre, auteur, annee, categorie, illustrateur):
        super().__init__(titre, auteur, annee, categorie)
        self.illustrateur = illustrateur
        self.disponible = True

    def afficheInfos(self):
        print(f"Titre : {self.titre}\nAuteur : {self.auteur}\nAnnée : {self.annee}\nCatégorie : {self.categorie}\nIllustrateur : {self.illustrateur}\nDisponible : {self.disponible}")

class Manga(Livres):
    def __init__(self, titre, auteur, annee, categorie, mangaka):
        super().__init__(titre, auteur, annee, categorie)
        self.mangaka = mangaka
        self.disponible = True
    
    def afficheInfos(self):
        print(f"Titre : {self.titre}\nAuteur : {self.auteur}\nAnnée : {self.annee}\nCatégorie : {self.categorie}\nMangaka : {self.mangaka}\nDisponible : {self.disponible}")

class livresFactory:
    @staticmethod
    def get_livre(type, *args, **kwargs):
        if type == 'bd':
            return BD(*args, **kwargs)
        elif type == 'manga':
            return Manga(*args, **kwargs)
        assert 0, 'Il n\'y a pas de ' + type

class Utilisateur:
    def __init__(self, nom, prenom, age):
        self.nom = nom
        self.prenom = prenom
        self.age = age

class Enfant(Utilisateur):
    def __init__(self, nom, prenom, age, ecole):
        super().__init__(nom, prenom, age)
        self.ecole = ecole

    def afficherEnfant(self):
        print(f"Nom : {self.nom}\nPrenom : {self.prenom}\nAge : {self.age}\nEcole : {self.ecole}\n")

class Adulte(Utilisateur):
    def __init__(self, nom, prenom, age, metier):
        super().__init__(nom, prenom, age)
        self.metier = metier

    def afficherAdulte(self):
        print(f"Nom : {self.nom}\nPrenom : {self.prenom}\nAge : {self.age}\nMetier : {self.metier}\n")

class UtilisateurFactory:
    @staticmethod
    def get_utilisateur(type, *args, **kwargs):
        if type == 'enfant':
            return Enfant(*args, **kwargs)
        elif type == 'adulte':
            return Adulte(*args, **kwargs)
        assert 0, 'Il n\'y a pas de ' + type



if __name__ == "__main__":
    
    B1 = Bibliotheque("Bibliotheque de Paris")
    B1.action()