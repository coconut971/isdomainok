"""Point d'entrée CLI pour okitsok"""

import argparse
import json
import sys

from .core import check_domains, DEFAULT_EXTENSIONS
from . import __version__


def supports_unicode() -> bool:
    """Vérifie si le terminal supporte l'Unicode/UTF-8"""
    encoding = sys.stdout.encoding
    if encoding is None:
        return False
    return encoding.lower() in ('utf-8', 'utf8')


def format_human_readable(results: dict) -> str:
    """
    Formate les résultats pour un affichage lisible par un humain.
    
    Args:
        results: Dictionnaire {domaine: statut}
        
    Returns:
        str: Résultats formatés avec alignement
    """
    if not results:
        return "Aucun résultat"
    
    # Déterminer si on peut utiliser les emojis
    use_emoji = supports_unicode()
    
    # Calculer la largeur maximale pour l'alignement
    max_domain_length = max(len(domain) for domain in results.keys())
    
    lines = []
    for domain, status in results.items():
        # Choisir le symbole approprié
        if status == "available":
            symbol = "[OK]" if not use_emoji else "✅"
            status_text = "available"
        elif status == "taken":
            symbol = "[XX]" if not use_emoji else "❌"
            status_text = "taken"
        else:
            symbol = "[??]" if not use_emoji else "❓"
            status_text = "unknown"
        
        # Formater la ligne avec alignement
        line = f"{domain.ljust(max_domain_length)}  {symbol} {status_text}"
        lines.append(line)
    
    return "\n".join(lines)


def format_json(results: dict) -> str:
    """
    Formate les résultats en JSON.
    
    Args:
        results: Dictionnaire {domaine: statut}
        
    Returns:
        str: JSON formaté
    """
    return json.dumps(results, indent=2, ensure_ascii=False)


def main():
    """Point d'entrée principal de la CLI"""
    # Configurer l'encodage UTF-8 si possible pour Windows
    if sys.platform == 'win32':
        try:
            # Essayer de configurer la console Windows en UTF-8
            if sys.stdout.encoding != 'utf-8':
                import io
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass  # Ignorer les erreurs de configuration
    
    parser = argparse.ArgumentParser(
        prog="okitsok",
        description="Verification rapide de disponibilite de noms de domaine via DNS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  okitsok opheora              Verifie opheora avec les extensions par defaut (.com, .fr, .io, .app)
  okitsok mysite --json        Affiche le resultat au format JSON
  okitsok example --timeout 5  Utilise un timeout de 5 secondes

Statuts possibles:
  available  [OK]  Le domaine semble disponible
  taken      [XX]  Le domaine est deja pris
  unknown    [??]  Impossible de determiner (erreur DNS, timeout, etc.)

Note: okitsok utilise uniquement le DNS pour verifier la disponibilite.
Les resultats sont indicatifs et peuvent ne pas refleter la disponibilite reelle
chez tous les registrars.
        """
    )
    
    parser.add_argument(
        "name",
        help="Nom de domaine à vérifier (sans extension)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Afficher le résultat au format JSON"
    )
    
    parser.add_argument(
        "--timeout",
        type=float,
        default=3.0,
        help="Timeout en secondes pour chaque requête DNS (défaut: 3.0)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    args = parser.parse_args()
    
    try:
        # Vérifier les domaines
        results = check_domains(
            base_name=args.name,
            extensions=DEFAULT_EXTENSIONS,
            timeout=args.timeout
        )
        
        # Afficher les résultats selon le format demandé
        if args.json:
            output = format_json(results)
        else:
            output = format_human_readable(results)
        
        print(output)
        
        # Code de sortie: 0 si au moins un domaine est disponible, 1 sinon
        has_available = any(status == "available" for status in results.values())
        sys.exit(0 if has_available else 1)
        
    except KeyboardInterrupt:
        print("\nInterrompu par l'utilisateur", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
