2. Les 4 Briques à Développer
# Brique 1 : L'Agent Historien (historian_agent.py)

C'est le seul agent de cette phase qui a besoin d'un outil externe (DuckDuckGo).

    Rôle : Chercher des anecdotes réelles, des lieux historiques, des tensions politiques ou des faits insolites de l'époque choisie.

    Outil : ddgs (DuckDuckGo Search) pour faire 2 à 3 requêtes ciblées.

    Sortie attendue : Un résumé structuré des faits historiques qui serviront d'ancrage réaliste à l'histoire.

# Brique 2 : L'Agent Bâtisseur d'Univers (world_builder_agent.py)

    Entrée : La fiche de l'Historien.

    Rôle : Transformer le contexte historique en terrain de jeu.

    Sortie attendue (JSON) :

        3 à 5 Lieux clés : Nom, description sensorielle, dangers, connexions avec les autres lieux.

        Le Bestiaire / Mobs : 3 à 5 types d'ennemis communs (ex: gardes corrompus, créatures, bandits) avec leurs stats de base (PV, attaque, faiblesse).

# Brique 3 : L'Agent Personnages (character_agent.py)

    Entrée : La fiche de l'Historien + Les Lieux créés par le Bâtisseur.

    Rôle : Peupler le monde avec des personnages mémorables rattachés aux lieux existants.

    Sortie attendue (JSON) :

        Les Protagonistes (PNJ Alliés / Neutres) : Nom, rôle, lieu où il se trouve, motivation, secret.

        Les Ennemis majeurs (Boss / Antagonistes) : Nom, objectif, lieu de repaire, stats de combat, garde rapprochée (liée aux mobs créés avant).

# Brique 4 : L'Agent Quête Principale (quest_agent.py)

    Entrée : Tout ce qui précède (Histoire + Lieux + Personnages).

    Rôle : Tisser le fil rouge qui relie les lieux et les personnages entre eux.

    Sortie attendue (JSON) :

        Synopsis & Accroche : Pourquoi le joueur démarre l'aventure.

        Les Étapes (Actes 1, 2, 3) : Objectifs précis, indices à trouver, PNJ à rencontrer.

        Dénouement : Confrontation finale et conditions de réussite ou d'échec.
