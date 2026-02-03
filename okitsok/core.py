"""Module d'orchestration des vérifications de domaines"""

from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .dns import check_domain_detailed


# Extensions par défaut à vérifier
DEFAULT_EXTENSIONS = [".com", ".fr", ".io", ".app"]


def check_domains(
    base_name: str,
    extensions: List[str] = None,
    timeout: float = 3.0,
    max_workers: int = 10
) -> Dict[str, str]:
    """
    Vérifie la disponibilité d'un nom de domaine avec plusieurs extensions.
    
    Args:
        base_name: Le nom de base (sans extension)
        extensions: Liste des extensions à vérifier (ex: ['.com', '.fr'])
        timeout: Timeout pour chaque requête DNS
        max_workers: Nombre maximum de workers pour les vérifications parallèles
        
    Returns:
        Dict[str, str]: Dictionnaire {domaine: statut}
    """
    if extensions is None:
        extensions = DEFAULT_EXTENSIONS
    
    results = {}
    
    # Créer la liste des domaines à vérifier
    domains = [f"{base_name}{ext}" for ext in extensions]
    
    # Vérifier les domaines en parallèle
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Soumettre toutes les tâches
        future_to_domain = {
            executor.submit(check_domain_detailed, domain, timeout): domain
            for domain in domains
        }
        
        # Récupérer les résultats au fur et à mesure
        for future in as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                status = future.result()
                results[domain] = status
            except Exception:
                results[domain] = "unknown"
    
    # Retourner les résultats dans l'ordre des extensions demandées
    ordered_results = {}
    for domain in domains:
        ordered_results[domain] = results.get(domain, "unknown")
    
    return ordered_results
