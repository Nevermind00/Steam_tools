
# from SPC import SPC
# Модули профиля
from .profileInformations.profile_ import Profile__
from .profileInformations.awards_ import Profile_Awards
from .profileInformations.friends_ import Friends
from .profileInformations.menu_ import ProfileMenu
#Модули магазина 
from .storeInformations.menu import WishlistMenu
from .storeInformations.wishlistFindGame import GameInfo
# from .storeInformations.wishlist_ import Wishlist

# Модули настроек
from .Settings.settingsMenu import SettingsMenu
#Модули торговой площадки
# from .marketInformations.menu_ import Menu

__all__ = ["Profile__", "ProfileMenu", "Friends", "Wishlist", "GameInfo", "WishlistMenu", "SettingsMenu"]

