from ddgs import DDGS


def search_web(query: str, max_results: int = 3) -> str:
    """Recherche une requête sur DuckDuckGo et retourne les extraits formatés."""
    try:
        # Lancement de la recherche texte
        results = DDGS().text(query, region="fr-fr", max_results=max_results)

        if not results:
            return f"Aucun résultat trouvé pour : {query}"

        formatted_results = []
        for r in results:
            title = r.get("title", "Sans titre")
            body = r.get("body", "")
            formatted_results.append(f"- {title} : {body}")

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Erreur DuckDuckGo : {e}"


if __name__ == "__main__":
    print(search_web("Teafae du mezfezt"))
