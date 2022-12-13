# IMPORT

import json # pour gérer le df
import regex as re # pour nettoyer le text des tweets
import matplotlib.pyplot as plt # pour afficher des graphiques
import random as rd # pour simuler le sentiment


# DATA D'EXEMPLE

fic = open('versailles_tweets_100.json', 'r')
df = json.load(fic)
fic.close()
liste_tweets = [] # stocke les objets Tweet


# CLASS PRINCIPAL

class Tweet:
    def __init__(self, auteur, text, hashtags=[], mentions=[], topics=[], sentiment=(0, 0)):
        self.auteur = auteur
        self.text = re.sub("[^a-zA-z0-9 @&é\"\'(§è!çà)\-#°\^¨$*€¥ôÔùÙ‰%`@#£=≠±+:÷\\/…•.;∞¿?,≤≥><]", "", text, 0)
        try:
            self.hashtags = [i['tag'] for i in hashtags['hashtags']]
        except:
            self.hashtags = []
        try:
            self.mentions = [i['username'] for i in mentions['mentions']]
        except:
            self.mentions = []
        try:
            temp = [i for i in topics] # crée une liste avec les dictionnaires de dictionnaires des topics
            temp2 = [] # crée une liste dans laquelle on ajoutera les sous-dictionnaires de clé 'domain' de temp
            temp3 = [] # crée une liste dans laquelle on ajoutera les valeurs de clé 'name' stocké dans les sous-dict 'domain'
            for x in temp:
                for y in x.keys():
                    if y == 'domain':
                        temp2.append(x[y])
            for x in temp2:
                for y in x .keys():
                    if y == 'name':
                        temp3.append(x[y])
            self.topics = temp3 # enfin, topics devient cette liste de valeurs
        except:
            self.topics = [] # sinon une liste vide
        self.sentiment = (round(rd.uniform(-1, 1), 2), round(rd.uniform(0, 1), 2)) # (polarité, subjectivité)


    # les méthodes de Tweet ne sont en fait pas directement affichable par la console, bien qu'on les ai créé
    # on n'était pas sûr de ce que demandait l'énoncé à ce niveau là
    def get_auteur(self):
        """Retourne l'auteur du tweet."""
        print("- Auteur.e du tweet :", self.auteur)
    

    def get_hashtags(self):
        """Retourne la liste des hashtags du tweet."""
        if bool(self.hashtags):
            print("- Hashtag(s) du tweet :", self.hashtags)
        else:
            print("- Ce tweet ne contient pas de hashtags.")


    def get_mentions(self):
        """Retourne la liste des mentions du tweet."""
        if bool(self.mentions):
            print("- Mention(s) du tweet :", self.mentions)
        else:
            print("- Ce tweet ne contient pas de mentions.")


    def get_sentiment(self):
        """Retourne les sentiments du tweet."""
        if -1 <= self.sentiment[0] < 0:
            polarité = "négatif"
        elif self.sentiment[0] == 0:
            polarité = "neutre"
        else:
            polarité = "positif"
        if 0 <= self.sentiment[1] < 0.5:
            subjectivité = "objectif"
        else:
            subjectivité = "subjectif"
        print("- Sentiment du tweet : {} et {}.".format(polarité, subjectivité))
    

    def get_topics(self):
        """Retourne la liste des topics du tweet."""
        if bool(self.topics):
            print("- Topic(s) du tweet :", self.topics)
        else:
            print("- Les topics ne sont pas disponibles pour ce tweet.")


# ITERATIONS DE LA CLASSE PRINCIPALE

# voici la structure à laquelle on fait référence dans le compte-rendu
# elle permet d'assigner une liste vide uniquement pour la propriété vide, et non pour les trois propriétés hashtags, mentions et topics en même temps
for tweet in df:
    try:
        liste_tweets.append(Tweet(tweet['_id'], tweet['text'], tweet['entities'], tweet['entities'], tweet['context_annotations']))
    except:
        try:
            liste_tweets.append(Tweet(tweet['_id'], tweet['text'], tweet['entities'], tweet['entities']))
        except:
            try:
                liste_tweets.append(Tweet(tweet['_id'], tweet['text'], tweet['entities'], tweet['context_annotations']))
            except:
                try:
                    liste_tweets.append(Tweet(tweet['_id'], tweet['text'], tweet['context_annotations']))
                except:
                    liste_tweets.append(Tweet(tweet['_id'], tweet['text']))


# FONCTIONS

def reset_zone_datterissage():
    """Supprime tout le text du fichier zone_d'atterissage.txt."""
    open("zone_d'atterissage.txt", "w").close()


def fill_zone_datterissage():
    """Remplit la zone d'atterissage avec tous les objets tweets de la liste de tweets."""
    reset_zone_datterissage()
    fic = open('zone_d\'atterissage.txt', 'a')
    for tweet in liste_tweets:
        fic.write(str(tweet.__dict__)+"\n")
    fic.close()


def get_top_k_hashtags(k):
    """Affiche le top k des hashtags les plus utilisé dans un bar chart."""
    temp = [x.hashtags for x in liste_tweets] # on récupère les listes de # de tous les tweets dans une liste
    temp = [x for y in temp for x in y] # on transforme la liste de liste en liste
    temp2 = dict() # on crée le dictionnaire qui stockera le # en clé et son occurence en valeur
    for i in temp:
        # population de temp2
        if i not in temp2.keys():
            temp2[i] = 1
        else:
            temp2[i] += 1 
    temp2 = list(map(list, temp2.items())) # on transforme le dictionnaire temp2 en liste de listes
    for x in temp2:
        x[0], x[1] = x[1], x[0] # on inverse la place du # et de son occurence pour pouvoir ranger la liste par ordre décroissant
    temp2.sort(reverse = True) # rangement par ordre décroissant
    try:
        a = temp2[k] # test de vérité pour faire échouer le try except directement si le # n'existe pas
        temp3 = [x[0] for x in temp2[:k]] # création des x et des y pour le graphe matplotlib
        temp4 = [y[1] for y in temp2[:k]]
        plt.bar(temp4, temp3)
        plt.xlabel("Hashtag")
        plt.ylabel("Nombre d'utilisation")
        plt.title("Top {} des hashtags les plus utilisés".format(k))
        plt.show()
    except:
        print("- Il n'y a pas", k, "hashtags différents. Essayer un nombre inférieur.")


def get_top_k_users(k):
    """Affiche le top k des utilisateurs ayant le plus posté dans un bar chart."""
    temp = [x.auteur for x in liste_tweets]
    temp2 = dict()
    for i in temp:
        if i not in temp2.keys():
            temp2[i] = 1
        else:
            temp2[i] += 1
    temp2 = list(map(list, temp2.items()))
    for x in temp2:
        x[0], x[1] = x[1], x[0]
    temp2.sort(reverse = True)
    try:
        a = temp2[k]
        temp3 = [x[0] for x in temp2[:k]]
        temp4 = [y[1] for y in temp2[:k]]
        plt.bar(temp4, temp3)
        plt.xlabel("Utilisateur")
        plt.ylabel("Nombre de posts")
        plt.title("Top {} des utilisateurs ayant le plus posté".format(k))
        plt.show()
    except:
        print("- Il n'y a pas", k, "utilisateurs différents. Essayer un nombre inférieur.")


def get_top_k_mentions(k):
    """Affiche le top k des utilisateurs les plus mentionné(e)s dans un bar chart."""
    temp = [x.mentions for x in liste_tweets]
    temp = [x for y in temp for x in y]
    temp2 = dict()
    for i in temp:
        if i not in temp2.keys():
            temp2[i] = 1
        else:
            temp2[i] += 1
    temp2 = list(map(list, temp2.items()))
    for x in temp2:
        x[0], x[1] = x[1], x[0]
    temp2.sort(reverse = True)
    try:
        a = temp2[k]
        temp3 = [x[0] for x in temp2[:k]]
        temp4 = [y[1] for y in temp2[:k]]
        plt.bar(temp4, temp3)
        plt.xlabel("Mention")
        plt.ylabel("Nombre d'utilisation")
        plt.title("Top {} des mentions les plus utilisées".format(k))
        plt.show()
    except:
        print("- Il n'y a pas", k, "utilisateurs mentionné(e)s différent(e)s. Essayer un nombre inférieur.")


def get_top_k_topics(k):
    temp = [x.topics for x in liste_tweets]
    temp = [x for y in temp for x in y]
    temp2 = dict()
    for i in temp:
        if i not in temp2.keys():
            temp2[i] = 1
        else:
            temp2[i] += 1
    temp2 = list(map(list, temp2.items()))
    for x in temp2:
        x[0], x[1] = x[1], x[0]
    temp2.sort(reverse = True)
    try:
        a = temp2[k]
        temp3 = [x[0] for x in temp2[:k]]
        temp4 = [y[1] for y in temp2[:k]]
        plt.bar(temp4, temp3)
        plt.xlabel("Topic")
        plt.ylabel("Nombre d'utilisation")
        plt.title("Top {} des topics les plus utilisées".format(k))
        plt.show()
    except:
        print("- Il n'y a pas", k, "topics différents. Essayer un nombre inférieur.")


def get_posts_per_user(user):
    """Affiche tous les tweets postés par l'utilisateur."""
    temp = []
    for tweet in liste_tweets:
        if str(user) == tweet.auteur:
            temp.append(tweet)
    if bool(temp):
        print("- Voici l'ensemble des tweets de l'utilisateur", user, ":")
        for x in temp:
            print("    -", x.text)
    else:
        print("- L'utilisateur n'a pas tweeté ou le nom d'utilisateur est incorrect.")


def get_nb_posts_per_user(user):
    """Affiche le nombre de tweets postés par l'utilisateur."""
    temp = []
    for tweet in liste_tweets:
        if str(user) == tweet.auteur:
            temp.append(tweet)
    if bool(temp):
        print("-", user, "a tweeté", len(temp), "fois.")
    else:
        print("- L'utilisateur n'a pas tweeté ou le nom d'utilisateur est incorrect.")


def get_nb_posts_per_hashtag(hashtag):
    """Affiche le nombre de tweet contenant le hashtag."""
    temp = []
    for tweet in liste_tweets:
        if hashtag in tweet.hashtags:
            temp.append(tweet)
    if bool(temp):
        print("- Il y a", len(temp), "tweet(s) mentionnant le hashtag", hashtag, "\b.")
    else:
        print("- Il n'y a pas de tweet contenant le hashtag", hashtag, "\b.")


def get_nb_posts_per_topic(topic):
    """Affiche le nombre de tweet contenant le topic."""
    temp = []
    for tweet in liste_tweets:
        if topic in tweet.topics:
            temp.append(tweet)
    if bool(temp):
        print("- Il y a", len(temp), "tweet(s) contenant le topic", topic, "\b.")
    else:
        print("- Il n'y a pas de tweet contenant le topic", topic, "\b.")


def get_posts_per_mention(mention):
    """Affiche les tweets contenant la mention."""
    temp = []
    for tweet in liste_tweets:
        if mention in tweet.mentions:
            temp.append(tweet)
    if bool(temp):
        print("- Voici l'ensemble des tweets mentionnant", mention, ":")
        for x in temp:
            print("    -", x.text)
    else:
        print("- Il n'y a pas de tweet mentionnant", mention, "\b.")


def get_users_per_hashtag(hashtag):
    """Affiche les utilisateurs ayant utilisé le hashtag spécifié."""
    temp = []
    for tweet in liste_tweets:
        if hashtag in tweet.hashtags:
            temp.append(tweet)
    if bool(temp):
        print("- Utilisateur(s) ayant utilisé le hashtag", hashtag, ":")
        for x in temp:
            print("    -", x.auteur)
    else:
        print("- Il n'y a pas d'utilisateur ayant utilisé le hashtag", hashtag, "\b.")


def get_mentions_per_user(user):
    """Affiche les mentions de l'utilisateur spécifié."""
    for tweet in liste_tweets:
        if tweet.auteur == str(user):
            temp = tweet
    try:
        if len(temp) == 0:
            print("- L'utilisateur", user, "n'a fait aucune mention ou n'existe pas.")
        print("- Mention(s) de l'utilisateur", user, ":")
        for x in temp.mentions:
            print("    -", x)
    except:
        print("- L'utilisateur", user, "n'a fait aucune mention ou n'existe pas.")


# CONSOLE

fill_zone_datterissage()
print("- InPoDa")
print("- Taper « commandes » pour afficher la liste des commandes.")
print("- Taper « quitter » pour quitter.")
while True:
    x = input("> ")
    if x == "quitter":
        break
    if x == "commandes":
        print("- [0] Afficher le top k des hashtags les plus utilisés.")
        print("- [1] Afficher le top k des utilisateurs ayant le plus posté.")
        print("- [2] Afficher le top k des mentions les plus utilisés.")
        print("- [3] Afficher le top k des topics les plus courants.")
        print("- [4] Afficher le nombre de posts d'un utilisateur.")
        print("- [5] Afficher le nombre de posts contenant un hashtag.")
        print("- [6] Afficher le nombre de posts contenant un topic.")
        print("- [7] Afficher les posts d'un utilisateur.")
        print("- [8] Afficher les posts contenant une mention.")
        print("- [9] Afficher les utilisateurs ayant utilisé un hashtag.")
        print("- [10] Afficher les mentions d'un utilisateur.")
    if x == "0":
        print("- Affichage du top k des hashtags les plus utilisés.")
        k = input("> Valeur de k : ")
        get_top_k_hashtags(int(k))
    if x == "1":
        print("- Affichage du top k des utilisateurs ayant le plus posté.")
        k = input("> Valeur de k : ")
        get_top_k_users(int(k))
    if x == "2":
        print("- Affichage du top k des mentions les plus utilisés.")
        k = input("> Valeur de k : ")
        get_top_k_mentions(int(k))
    if x == "3":
        print("- Affichage du top k des topics les plus courants.")
        k = input("> Valeur de k : ")
        get_top_k_topics(int(k))
    if x == "4":
        print("- Affichage du nombre de posts d'un utilisateur.")
        k = input("> Nom de l'utilisateur : ")
        get_nb_posts_per_user(k)
    if x == "5":
        print("- Affichage du nombre de posts contenant un hashtag.")
        k = input("> Hashtag cherché : ")
        get_nb_posts_per_hashtag(k)
    if x == "6":
        print("- Affichage du nombre de posts contenant un topic.")
        k = input("> Topic cherché : ")
        get_nb_posts_per_topic(k)
    if x == "7":
        print("- Affichage des posts d'un utilisateur.")
        k = input("> Nom de l'utilisateur : ")
        get_posts_per_user(k)
    if x == "8":
        print("- Affichage des posts contenant une mention.")
        k = input("> Mention cherché : ")
        get_posts_per_mention(k)
    if x == "9":
        print("- Affichage des utilisateurs ayant utilisé un hashtag.")
        k = input("> Hashtag cherché : ")
        get_users_per_hashtag(k)
    if x == "10":
        print("- Affichage des mentions d'un utilisateur.")
        k = input("> Utilisateur cherché : ")
        get_mentions_per_user(k)
