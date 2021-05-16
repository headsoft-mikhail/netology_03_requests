import requests
from tokens import SUPERHERO_TOKEN as sh_token


class Superhero:
    def __init__(self, name):
        self.name = name
        self.stats = self.get_hero_stats(self.name)

    def get_hero_stats(self, heroname):
        resp = requests.get("https://superheroapi.com/api/" + sh_token + "/search/" + self.name)
        if resp.status_code != 200:
            print(f"Error occured with {heroname}: status code {resp.status_code}")
            return None
        elif resp.json()["response"] != "success":
            print(f"Error occured with {heroname}: {resp.json()['error']}")
            return None
        else:
            for result in resp.json()['results']:
                if result['name'] == heroname:
                    print(f"Got stats for {heroname}")
                    return result['powerstats']


if __name__ == '__main__':
    hero_name_list = ["Hulk", "Megan", "Captain America", "Thanos", "She-Hulk"]
    compare_hero_dict = {}
    parameter = "intelligence"
    #parameter = "strength"

    # get all heroes by the list
    for hero_name in hero_name_list:
        hero = Superhero(hero_name)
        if hero.stats is not None and parameter in hero.stats:
            compare_hero_dict[hero.name] = int(hero.stats[parameter])

    # search max value and all max value owners
    max_param = compare_hero_dict[max(compare_hero_dict, key=compare_hero_dict.get)]
    best_heroes = []
    for hero in compare_hero_dict.keys():
        if compare_hero_dict[hero] == max_param:
            best_heroes.append(hero)

    # result output
    result_phrase = f"{', '.join(best_heroes,)} " \
                    f"has {parameter} of " \
                    f"{max_param}, " \
                    f"this superhero is the best!"
    if len(best_heroes) > 1:
        result_phrase = f"{' ,'.join(best_heroes, )} " \
                        f"have {parameter} of " \
                        f"{max_param}, " \
                        f"these superheroes are the best!"
    print(result_phrase)
