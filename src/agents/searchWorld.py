import textwrap

from src.llm_call import LLMClient
from src.model.struct_model import WorldDescription
from src.tool_search import search_web

MAX_ITER = 3


class LlmMaxIteration(Exception):
    """To much llm iteration."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HistorianAgent:
    def __init__(self, userPrompt):
        self.model = "mistral"
        self.userPrompt = userPrompt
        self.llm = LLMClient(model=self.model, temperature=0.7)
        self.worldDescription = {
            "era_and_location": "",
            "context": "",
            "atmosphere_keywords": "",
            "real_landmarks": "",
            "factions_and_tensions": "",
            "folklore_and_secrets": "",
            "ennemie": "",
            "player": "",
        }

    def _format_current_context(self) -> str:
        """Met en forme uniquement les champs déjà générés pour servir de mémoire propre."""
        filled_parts = []
        for field, value in self.worldDescription.items():
            if value.strip():
                filled_parts.append(f"- **{field}** : {value}")

        if not filled_parts:
            return "Aucun élément établi pour le moment (c'est le premier point)."

        return "\n".join(filled_parts)

    def _build_search_input_prompt(self, description: str) -> tuple[str, str]:
        system_prompt = textwrap.dedent("""\
            Tu es un moteur de génération de requêtes DuckDuckGo.
            Ta seule tâche est de convertir un objectif de recherche en une requête courte de 3 à 5 mots-clés efficaces.

            Règles strictes :
            - Réponds UNIQUEMENT avec les mots-clés de recherche.
            - N'écris AUCUNE phrase, AUCUNE introduction, AUCUN guillemet ni ponctuation.
            - Utilise des termes précis (noms propres, lieux, concepts clés).

            Exemple :
            Univers : France, 1789, ambiance sombre et ésotérique
            Objectif : 2 à 4 légendes urbaines, rumeurs occultes ou sociétés secrètes
            Réponse attendue : Paris 1789 sociétés secrètes occultisme""")

        user_prompt = textwrap.dedent(f"""\
            Univers : {self.userPrompt}
            Objectif : {description}
            Requête :""")

        return (system_prompt, user_prompt)

    def _build_search_output_prompt(
        self, description: str, search_result: str
    ) -> tuple[str, str]:
        system_prompt = textwrap.dedent("""\
            Tu es un documentaliste expert pour jeu de rôle.
            Ta tâche est d'extraire et synthétiser uniquement les informations pertinentes d'un résultat de recherche web pour répondre à un objectif précis, tout en restant cohérent avec ce qui a déjà été établi sur le monde.

            Règles strictes :
            - Rédige une synthèse dense, factuelle et directement exploitable (2 à 3 phrases ou puces maximum).
            - Reste strictement fidèle aux informations fournies et à l'univers demandé.
            - Évite de répéter ce qui est déjà écrit dans le contexte établi.
            - N'écris AUCUNE phrase d'introduction ou de conclusion (pas de "Voici la synthèse...", "D'après les résultats...").
            - Si les résultats sont pauvres, garde uniquement les éléments utiles sans inventer de faits extérieurs.""")

        current_context = self._format_current_context()

        user_prompt = textwrap.dedent(f"""\
            Univers : {self.userPrompt}

            Éléments déjà établis sur ce monde :
            {current_context}

            Objectif à remplir maintenant : {description}

            Résultats de recherche bruts :
            {search_result}

            Synthèse :""")

        return (system_prompt, user_prompt)

    def getFields(self):
        for field in self.worldDescription:
            web_response = ""
            count = 0
            while (web_response == "" or
                    "Erreur DuckDuckGo" in web_response):
                description = WorldDescription.model_fields[field].description
                system_prompt, user_prompt = self._build_search_input_prompt(
                    description=description
                )
                search = self.llm.generate_text(
                    system_prompt, user_prompt
                ).strip('"\' \n.')
                web_response = search_web(search)
                if count >= MAX_ITER:
                    raise LlmMaxIteration("To much llm iteration")
                count += 1

            system_prompt, user_prompt = self._build_search_output_prompt(
                description, web_response
            )
            self.worldDescription[field] = self.llm.generate_text(
                system_prompt, user_prompt
            ).strip('"\' \n')
        for field in self.worldDescription:
            print("[" + field + "] -> ", self.worldDescription[field], "\n\n")


if __name__ == "__main__":
    h = HistorianAgent("Star wars")
    h.getFields()
