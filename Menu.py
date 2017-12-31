class Menu():
    def __init__(self, data, id, parent_id = None, child_ids = [], root = False):
        self.root = root               # True if menu is a root, False otherwise
        self.data = data               # The data held in a menu
        self.id = id                   # The ID of a menu
        self.child_ids = child_ids     # The IDs of the children of a menu
        self.children = []             # A list of Node objects that represent the children of a menu
        self.parent_id = parent_id     # The ID of the parent menu. ID is None if menu is a root.

    def add_child(self, menu):
        self.children.append(menu)

    def is_cyclic(self, visited = list()):
        """
        Recursively finds whether or not self is cyclic.

        This function works by traversing all children and storing which menus have been visited.
        If a menu is visited twice, then the tree is cyclic at some point.
        :param visited: a list of already visited menu objects.
        :return: True if cyclic, False otherwise
        """
        if self in visited:
            return True
        if self.children == []:
            return False
        visited.append(self)
        for child in self.children:
            if child.is_cyclic(visited=visited):
                return True
        return False

    def __str__(self):
        """
        :return: String representation of a Node object, in the format "id data"
        """
        return str(self.id) + " " + self.data

    def __repr__(self):
        """
        :return: String representation of a Node object, in the format "id data"
        """
        return self.__str__()

    def all_children(self, return_list=set(), visited=[]):
        """
        Finds all child menus of a menu.
        :param return_list: the final list to return. Nodes are continually added when found
        :param visited: a list of already visited menus. Once a menu is visited twice, we return.
        :return: a list of menus that are children of the calling menu
        """
        if self.children == [] or self in visited:
            return
        visited.append(self)
        for child in self.children:
            return_list.add(child)
            child.all_children(return_list=return_list, visited=visited)
        return return_list
