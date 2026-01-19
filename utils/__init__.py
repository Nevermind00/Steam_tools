# Модули профиля
from .profileInformations.profile_ import Profile__
from .profileInformations.awards_ import Profile_Awards
from .profileInformations.friends_ import Friends
from .profileInformations.menu_ import ProfileMenu
#Модули магазина 
from .storeInformations.menu import WishlistMenu
#Модули торговой площадки
# from .marketInformations.menu_ import Menu

__all__ = ["Profile__", "Awards__", "ProfileMenu", "Friends", "WishlistMenu"]