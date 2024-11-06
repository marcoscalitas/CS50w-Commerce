from .models import Listing

def watchlist_listings_count(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        # Conta quantos listings estão na watchlist do usuário autenticado
        watchlist_count = Listing.objects.filter(watchlist=request.user).count()
    else:
        watchlist_count = 0  # Se o usuário não estiver autenticado, retorna 0
    
    return {'watchlist_count': watchlist_count}
