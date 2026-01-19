import requests
import os

class Friends(): 
    def __init__(self):

        #Передавать параметр steamid из модуля profile_.py 
        self.steamid = "76561199081326623"
        self.token = os.getenv("API_KEY")

        self.steamid_friends = self.friends_list_steamid(steamid=self.steamid, token=self.token)

        self.friends_info(steamid_friends=self.steamid_friends, token=self.token)


    def friends_info(self, steamid_friends, token):
        if not steamid_friends:
            print("The friends list is empty... =(")
            return
        
        # Объединяем все SteamID через запятую для одного запроса
        steamids_string = ",".join(str(friend) for friend in steamid_friends)
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={token}&steamids={steamids_string}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            players = data["response"]["players"]
            friends_count = 0
            
            for player in players:
                friends_count += 1
                #Получение никнейма
                self.nickname = player["personaname"]
                #Получение steamid
                # self.id = player["steamid"]
                #Получение ссылки на профиль
                # self.profileURL = player["profileurl"]

                print(f"{friends_count}. {self.nickname}")
            print(f"Total Friends Count: {friends_count}")

            
        except requests.exceptions.RequestException as e:
            print(e)
        except KeyError as e:
            print(e)
        
    def friends_list_steamid(self, steamid, token):
        try:
            friends_list_url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={token}&steamid={steamid}&relationship=friend"
            response = requests.get(friends_list_url)
            response.raise_for_status()  
            
            data = response.json()
            friends_list = data["friendslist"]["friends"]
            
            steamids = []
            for friend in friends_list:
                steam_id = friend["steamid"]
                steamids.append(steam_id)
            return steamids  
            
        except requests.exceptions.RequestException as e:
            print(e)
        except KeyError as e:
            print(e)
        except Exception as e:
            print(e)
        
        return []

if __name__ == "__main__":
    Friends()