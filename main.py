"""
Point d'entrée principal de l'API de gestion de cyclisme.

Ce module configure l'application FastAPI et intègre tous les routeurs
pour les différentes fonctionnalités de l'API : gestion des utilisateurs,
des athlètes, des performances et des statistiques.

Modules importés:
    - FastAPI: Framework principal pour la création de l'API
    - APIRouter: Gestionnaire de routes pour organiser les endpoints
    - endpoints: Module contenant tous les routeurs spécifiques
        - athletes: Gestion des athlètes
        - users: Gestion des utilisateurs
        - performances: Gestion des performances
        - stats: Gestion des statistiques
"""

from fastapi import FastAPI, APIRouter
from endpoints import athletes, users, performances, stats

# Création de l'instance principale de l'application
app = FastAPI(
    title="Cycling Management API",
    description="""
    API de gestion pour les athlètes cyclistes, leurs performances et leurs statistiques.
    Permet la gestion des utilisateurs (athlètes, coachs, administrateurs),
    le suivi des performances et l'analyse statistique.
    """,
    version="1.0.0"
)

# Intégration des différents routeurs
app.include_router(users.router,tags=["Utilisateurs"])
app.include_router(athletes.router,tags=["Athlètes"])
app.include_router(performances.router,tags=["Performances"])
app.include_router(stats.router,tags=["Statistiques"])

@app.get("/")
def home():
    """Page d'accueil de l'API.

    Returns:
        dict: Message de bienvenue pour l'API

    Example:
        >>> response = home()
        >>> print(response)
        {"message": "Welcome to the Cycling management API"}
    """
    return {"message": "Welcome to the Cycling management API"}

"""
Notes sur l'utilisation de l'API:

1. Authentication:
   - L'API utilise une authentification JWT
   - Les tokens sont requis pour la plupart des endpoints
   - Différents niveaux d'accès selon les rôles (athlète, coach, admin)

2. Structure des routes:
   - /user/: Gestion des utilisateurs et authentification
   - /athletes/: Gestion des profils d'athlètes
   - /performances/: Suivi des performances
   - /stats/: Analyses statistiques

3. Documentation:
   - Documentation interactive disponible sur /docs
   - Documentation ReDoc disponible sur /redoc

4. Sécurité:
   - Validation des données via Pydantic
   - Gestion des permissions basée sur les rôles
   - Protection contre les injections SQL
"""