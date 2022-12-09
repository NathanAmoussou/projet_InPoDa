import json # pour gérer le df
import regex as re # pour nettoyer le text des tweets


fic = open('versailles_tweets_100.json', 'r')
df = json.load(fic)
fic.close()
liste_tweets = [] # stocke les objets Tweet


class Tweet:
    def __init__(self, auteur, text, hashtags=[], mentions=[]):
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


    def get_auteur(self):
        print("Auteur.e du tweet :", self.auteur)
    

    def get_hashtags(self):
        if bool(self.hashtags):
            print("Hashtag(s) du tweet :", self.hashtags)
        else:
            print("Ce tweet ne contient pas de hashtags.")


    def get_mentions(self):
        if bool(self.mentions):
            print("Mention(s) du tweet :", self.mentions)
        else:
            print("Ce tweet ne contient pas de mentions.")


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
    """Affiche le top k des hashtags les plus utilisé."""
    temp = [x.hashtags for x in liste_tweets]
    temp = [x for y in temp for x in y]
    temp2 = dict()
    for i in temp:
        if i not in temp2.keys():
            temp2[i] = 1
        else:
            temp2[i] += 1
    temp2 = list(map(list, temp2.items())) # transforme le dictionnaire temp en liste de listes
    for x in temp2:
        x[0], x[1] = x[1], x[0]
    temp2.sort(reverse = True)
    try:
        a = temp2[k]
        print("Top", k, "des hashtags les plus utilisés :")
        for i in range(k):
            print(temp2[i][1], "utilisé", temp2[i][0], "fois")
    except:
        print("Il n'y a pas", k, "hashtags différents. Essayer un nombre inférieur.")



for tweet in df:
    try:
        liste_tweets.append(Tweet(tweet['_id'], tweet['text'], tweet['entities'], tweet['entities']))
    except:
        liste_tweets.append(Tweet(tweet['_id'], tweet['text']))

fill_zone_datterissage()
get_top_k_hashtags(20)
