from pydantic import BaseModel, Field


class WorldDescription(BaseModel):
    era_and_location: str = Field(
        description="Époque exacte et zone géographique principale, ex: 'Paris, Automne 1789'"
    )
    context: str = Field(
        description="Résumé détaillé du contexte historique, des événements récents et de la situation politique."
    )
    atmosphere_keywords: list[str] = Field(
        description="3 à 5 adjectifs ou mots-clés définissant l'ambiance sensorielle et émotionnelle."
    )
    real_landmarks: list[str] = Field(
        description="4 à 7 lieux réels emblématiques de cette époque qui pourront servir d'inspiration."
    )
    factions_and_tensions: list[str] = Field(
        description="2 à 3 factions, groupes sociaux ou pouvoirs en conflit avec leurs objectifs."
    )
    folklore_and_secrets: list[str] = Field(
        description="2 à 3 légendes urbaines, rumeurs, sociétés ou faits insolites réels."
    )
    ennemie: list[str] = Field(
        description="5 à 8 différents ennemis, milices, bandits ou créatures"
    )
    player: list[str] = Field(
        description="5 à 8 personnage ou créature que pourrait incarner un joueur"
    )


# ========== BRIQUE 2 : BÂTISSEUR D'UNIVERS ==========
class Location(BaseModel):
    id: str = Field(description="Identifiant unique court en \
        snake_case, ex: catacombes_paris")
    name: str
    sensory_description: str = Field(description="Ce qu'on voit, \
        entend, sent sur place")
    dangers: list[str]
    connected_location_ids: list[str] = Field(description="IDs des autres \
        lieux accessibles depuis ici")


class Mob(BaseModel):
    id: str = Field(description="Identifiant unique court, ex: garde_corrompu")
    name: str
    description: str
    hp: int
    attack: int
    weakness: str


class WorldBuildingOutput(BaseModel):
    locations: list[Location]
    mobs: list[Mob]


# ========== BRIQUE 3 : PERSONNAGES ==========
class AllyNPC(BaseModel):
    name: str
    role: str
    location_id: str = Field(description="Doit correspondre exactement \
        à l'id d'un Location")
    motivation: str
    secret: str


class BossEnemy(BaseModel):
    name: str
    title: str
    objective: str
    lair_location_id: str = Field(description="Doit correspondre exactement \
        à l'id d'un Location")
    hp: int
    attack: int
    weakness: str
    minion_mob_id: str = Field(description="Doit correspondre exactement \
        à l'id d'un Mob")


class CharactersOutput(BaseModel):
    allies: list[AllyNPC]
    bosses: list[BossEnemy]


# ========== BRIQUE 4 : QUÊTE PRINCIPALE ==========
class QuestAct(BaseModel):
    act_number: int
    title: str
    objectives: list[str]
    clues_to_find: list[str]
    key_npc_names: list[str]
    target_location_ids: list[str]


class MainQuestOutput(BaseModel):
    title: str
    synopsis: str
    starting_hook: str = Field(description="Pourquoi et comment le \
        joueur démarre l'aventure")
    acts: list[QuestAct] = Field(description="Découpage précis en 3 actes")
    climax_and_resolution: str
    victory_conditions: list[str]
    failure_conditions: list[str]


# ========== BIBLE FINALE (world_state.json) ==========
class WorldBible(BaseModel):
    user_prompt: str
    historical_context: str
    world: WorldBuildingOutput
    characters: CharactersOutput
    main_quest: MainQuestOutput
