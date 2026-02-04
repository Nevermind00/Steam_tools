from bs4 import BeautifulSoup as bs
import requests
import re

class Profile_Awards():
    def __init__(self):
        ...

    def Profile(self, url_awards):
        
        self.steam_profile_url_awards = f"{url_awards}"
        self.responce_awards   = requests.get(self.steam_profile_url_awards)
        self.html_awards       = self.responce_awards.text
        self.awards            = bs(self.html_awards, 'lxml')
        

        self.profile_awards_received = None
        self.profile_awards_given    = None
        self.profile_awards_header_subtitle = self.awards.find_all("div", class_="profile_awards_header_subtitle")

#====================================================================================
#ADWARDS RECEIVED
#====================================================================================
    def Get_Awards_Received(self):
        if self.awards is None:
            return "Profile not found"
        try:
            profile_awards_received = self.profile_awards_header_subtitle[0].text
            return profile_awards_received
        except Exception as e:
            return f"Error: {e}"
#====================================================================================
#ADWARDS GIVEN
#====================================================================================
    def Get_Awards_Given(self):
        if self.awards is None:
            return "Profile not found"
        try:
            profile_awards_given = self.profile_awards_header_subtitle[1].text
            return profile_awards_given
        except Exception as e:
            return f"Error: {e}"

    
if __name__ == "__main__":
    print("Run main file")