import requests
import json
from JsonEncoder import JsonEncoder
from Menu import Menu


"""
This is my entry for the Shopify Backend Internship challenge for Summer 2018.

There are several different ways to approach this problem. My solution uses a Menu object
that functions as a directed graph/n-ary tree.

To use, just run the program with the Python interpreter, and it will automatically
spit out the values from both id=1 and id=2 challenges, as given on the challenge page.

Other solutions would be to use LinkedLists, but that would only work if a Menu entry were
only allowed one child.

@author Ensar Ilyas

"""

def get_data(challenge_num=1):
    """
    Pulls Menus from the challenge API and returns it in a dictionary.
    :param challenge_num: the challenge number to pull from, represented in the API
                          by the parameter id
    :return: a dict of menus from the API
    """
    trees = {}
    i = 0

    # Although bad practice, we use a while True loop here and break
    # out of loop when necessary (i.e. when there are no more menus)
    # This is because we don't know on loop iteration whether or not the API has returned something.
    while True:
        r = requests.get("https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id="
                         + str(challenge_num) + "&page=" + str(i))
        json_text = json.loads(r.text)
        if not json_text['menus']:
            break
        for value in json_text['menus']:
            is_root = False

            if "parent_id" not in value:
                is_root = True
                value['parent_id'] = None

            menu = Menu(value['data'], value['id'], child_ids=value['child_ids'], parent_id=value['parent_id'],
                        root=is_root)
            trees[value['id']] = menu # Replaces the ID entry in the dictionary with a Menu object

        i+=1
    return trees

def create_structures(menus):
    """
    Creates Menu structures by adding children to their respective parents.
    :param menus: A list of menus
    """
    for key, value in menus.items():
        for id in value.child_ids:
            value.add_child(menus[id])

def build_response(menus):
    """
    Builds the response for the final output.
    :param menus: A dict of menus that represent the menus pulled from the API.
    :return: a JSON-serialized string that represent the menus
    """
    response = dict()
    response["True"] = list()
    response["False"] = list()

    # Runs through all roots and finds their validity + children
    for menu in menus.values():
        if menu.root:
            validity = str(menu.is_cyclic())
            children = menu.all_children(return_list = set(), visited=[])
            response[validity].append({"root_id": menu.id})
            response[validity][-1]['children'] = children.copy()
    response['valid_menus'] = response.pop("False")
    response['invalid_menus'] = response.pop("True")
    return response

def build_json(resp):
    return json.dumps(resp, cls=JsonEncoder)

if __name__ == "__main__":
    for i in range(1,3):
        menus = get_data(i)
        create_structures(menus)
        response = build_response(menus)
        response = build_json(response)
        print(response)