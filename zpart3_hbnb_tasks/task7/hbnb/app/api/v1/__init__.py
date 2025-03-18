from .auth import api as auth_ns
from .users import api as users_ns
from .places import api as places_ns
from .reviews import api as reviews_ns
from .amenities import api as amenities_ns

__all__ = ['auth_ns', 'users_ns', 'places_ns', 'reviews_ns', 'amenities_ns']

