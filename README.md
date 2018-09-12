
# Nemopay-mini-cli
Outil d'importation de droits sur Nemopay.

Dans la version actuelle il faut recuperer un id de session existant en se connectant manuellement sur le back office nemopay.

## Utilisation
```bash
python nemopay-mini-cli.py -i <inputfile> -a <addWalletToGroup|addUserToGroup|addWalletRight|addUserRight> -u <casUsername> -p <casPassword> [-f <fundationid>]
```

* **-i ou --inputfile** : fichier au format CSV contenant les modifications à apporter (structure du fichier plus bas)
* **-a ou --action**    : action à executer
* **-u ou --username** : Login a utiliser pour se connecter au syteme via CAS
* **-p ou --password** : Mot de passe a utiliser pour se connecter au syteme via CAS
* **-f ou --fundation** : Id de la fondation sur laquelle mettre les droits (dans le cas de l'action **addRight**) s'il est omis la permission s'applique à tout le système 

## Structure du fichier d'entrée
 Les entêtes ne sont pas à recopier dans le fichier d'entrée, ils sont donnés ici à titre d'explication.

### Action addWalletRight ou addUserRight
Noter que le paramètre -f permet de ne donner les permission que sur 1 fondation particulière.

| Prenom | Nom | Login | Permission |
|--|--|--|--|
| Cesar | Richard | cerichar | SALES |
| Cesar | Richard | cerichar | STAFF |
| Quentin | Richard | qrichard | SALES |

Rappel des droits disponibles pour les wallets :
1. **SALES** : Vente
2. **STAFF** : Responsable des lieux ou il peut vendre
3. **RELOAD** : Rechargement
4. **ACCESSCONTROL** : Contrôle des accès
5. **ASSISTANCE** : Assistance
6. **PAIRING** : Appairage 
7. **STOCK** : Gestion des stocks 
8. **EDITACCESSRIGHT** : Édition des accès
9. **ADMIN** : Tous les droits

Rappel des droits disponibles pour les users :
1. **POSS3** : Vente Physique
2. **MESSAGE** : Gestion des messages personnalisés
3. **STATS** : Consultations des statistiques de vente
4. **STOCKS** : Gestion des stocks
5. **MAKEINVENTORIES** : Réalisation d'inventaires
6. **GESSALES** : Gestion des ventes
7. **STAFF** : Responsable des lieux ou il peut vendre (eg: responsable de bar)
8. **GESWIFICONFIGS** : Gestion des réseaux wifi

----------


### Action addWalletToGroup ou addUserToGroup

| Prenom | Nom | Login | Id du groupe |
|--|--|--|--|
| Cesar | Richard | cerichar | 4 |
| Quentin | Richard | qrichard | 3 |

