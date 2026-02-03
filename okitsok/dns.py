"""Module de résolution DNS pour vérifier la disponibilité des domaines"""

import socket
import sys

try:
    import dns.resolver
    import dns.exception
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False


def check_domain_with_dnspython(domain: str, timeout: float = 3.0) -> str:
    """
    Vérifie un domaine en utilisant dnspython pour interroger NS, SOA, puis A/AAAA.
    
    Args:
        domain: Le nom de domaine complet à vérifier
        timeout: Timeout en secondes pour les requêtes DNS
        
    Returns:
        str: 'available', 'taken', ou 'unknown'
    """
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    
    # Liste des types d'enregistrements à vérifier, par ordre de priorité
    record_types = ['NS', 'SOA', 'A', 'AAAA']
    
    for record_type in record_types:
        try:
            answers = resolver.resolve(domain, record_type)
            if answers:
                # Le domaine a des enregistrements DNS, il est pris
                return "taken"
        except dns.resolver.NXDOMAIN:
            # NXDOMAIN = le domaine n'existe pas
            return "available"
        except dns.resolver.NoAnswer:
            # Pas de réponse pour ce type d'enregistrement, continuer
            continue
        except dns.resolver.NoNameservers:
            # Serveurs de noms inaccessibles
            return "unknown"
        except dns.exception.Timeout:
            return "unknown"
        except Exception:
            # Autres erreurs DNS
            continue
    
    # Si aucun enregistrement trouvé mais pas d'erreur NXDOMAIN, considérer comme unknown
    return "unknown"


def check_domain_with_socket(domain: str, timeout: float = 3.0) -> str:
    """
    Fallback utilisant socket.getaddrinfo (vérifie seulement A/AAAA).
    
    Args:
        domain: Le nom de domaine complet à vérifier
        timeout: Timeout en secondes pour les requêtes DNS
        
    Returns:
        str: 'available', 'taken', ou 'unknown'
    """
    original_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    
    try:
        result = socket.getaddrinfo(domain, None)
        if result:
            return "taken"
        return "unknown"
    except socket.gaierror as e:
        error_code = getattr(e, 'errno', None)
        error_msg = str(e).lower()
        
        if sys.platform == 'win32':
            if error_code == 11001 or "no such host is known" in error_msg:
                return "available"
            if "getaddrinfo failed" in error_msg:
                return "unknown"
        else:
            if error_code == socket.EAI_NONAME or \
               "name or service not known" in error_msg or \
               "nodename nor servname provided" in error_msg:
                return "available"
        
        return "unknown"
    except socket.timeout:
        return "unknown"
    except Exception:
        return "unknown"
    finally:
        socket.setdefaulttimeout(original_timeout)


def check_domain_detailed(domain: str, timeout: float = 3.0) -> str:
    """
    Vérifie la disponibilité d'un domaine via DNS.
    
    Utilise dnspython si disponible (vérifie NS, SOA, A, AAAA),
    sinon utilise socket comme fallback (vérifie seulement A/AAAA).
    
    Args:
        domain: Le nom de domaine complet à vérifier
        timeout: Timeout en secondes pour les requêtes DNS
        
    Returns:
        str: 'available', 'taken', ou 'unknown'
    """
    if HAS_DNSPYTHON:
        return check_domain_with_dnspython(domain, timeout)
    else:
        return check_domain_with_socket(domain, timeout)
