# TD-ransomware
 TD ransomware - CyberSecurity

Q1 :

    Nom de l'algorithme : Cryptage XOR
    Pas vraiment, en possédant un fichier à la fois en clair et encrypté, nous pouvons retrouver la clef.

Q2 : 

    Car nous en avons besoin pour chiffrer les fichiers par la suite
    HMAC est utilisé pour vérifier l'intégrité des données

Q3 :

    Eviter d'ecrire dans un fichier contenant déjà qqc et 
    de perdre ainsi le token.
    Eviter de pwned une nouvelle fois une victime

Q4 :

    Pour vérifier que la clef est la bonne, nous demandons au serveur CNC

B1 :

    Envoie d'une requête POST avec tous les fichiers du clients.
    Une fois reçus, les fichiers sont stockés dans le dossier correspondant au token.

B2: 
    
    En effectuant une opération XOR sur un fichier clair et le même crypté, nous obtenons 
    la clef répété x fois pour atteindre la taille du fichier
    Voir sources/chiffrement_answer.py

B3: 

    Utilisation de Fernet
    Fernet garantie que le message crypté ne peut ếtre lu ou manipulé sans la clef.

B4: 

    pyinstaller --onefile --windowed source/ransomware.py

B5: 

    Le binaire s'enregistre dans le dossier dist


Erreur pour l'execution du binaire ransomware :
    Besoin de GLIBC 2.35 mais GLIBC 2.31 sur la machine cliente
