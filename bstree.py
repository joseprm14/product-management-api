class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)
    

    def _insert(self, current, key, value):
        if key < current.key:
            if current.left is None:
                current.left = Node(key, value)
            else:
                self._insert(current.left, key, value)
        elif key > current.key:
            if current.right is None:
                current.right = Node(key, value)
            else:
                self._insert(current.right, key, value)
        else:
            raise ValueError('Duplicate keys are not allowed')

    
    def search(self, key):
        return self._search(self.root, key)
    
    
    def _search(self, current, key):
        if current is None:
            return None
        if key == current.key:
            return current.value
        elif key < current.key:
            return self._search(current.left, key)
        else:
            return self._search(current.right, key)


    
    def delete(self, key):
        if self.root is None:
            return
        elif self.root.key == key:
            if self.left is None and self.right is None:
                self.root = None
                return
            elif self.left is None:
                self.root = self.root.right
                return
            elif self.right is None:
                self.root = self.root.left
                return
            else:
                maxValNode = self.maxValue(self.root.left)
                self.root.key = maxValNode.key
                self.root.value = maxValNode.value
                self._delete(self.root.left, self.root, maxValNode.key)
                return
        elif key < self.root.key:
            self._delete(self.root.left, self.root, key)
            return
        elif key > self.root.key:
            self._delete(self.root.right, self.root, key)
            return


    def _delete(self, current, parent, key):
        if current.key != key:
            if current.left is None and current.right is None:
                return
            elif key < current.key:
                self._delete(current.left, current, key)
                return
            elif key > current.key:
                self._delete(current.right, current, key)
                return
        else:
            if current.left is None and current.right is None:
                if current.key < parent.key:
                    parent.left = None
                    return
                elif current.key > parent.key:
                    parent.right = None
                    return
            elif current.left is None:
                if current.key < parent.key:
                    parent.left = current.right
                    return
                elif current.key > parent.key:
                    parent.right = current.right
                    return
            elif current.right is None:
                if current.key < parent.key:
                    parent.left = current.left
                    return
                elif current.key > parent.key:
                    parent.right = current.left
                    return
            else:
                maxValNode = self.maxValue(current.left)
                current.key = maxValNode.key
                current.value = maxValNode.value
                self._delete(current.left, current, maxValNode.key)
                return
            

    def maxValue(self, current):
        if current.right is None:
            return current
        else:
            return self.maxValue(current.right)


    def list_tree(self):
        """Lists the tree structure in an in-order traversal."""
        if self.root is None:
            return []
        else:
            return self._list_in_order(self.root, [])


    def _list_in_order(self, current, ordered_list):
        if current is not None:
            ordered_list = self._list_in_order(current.left, ordered_list)
            ordered_list.append({'id': current.key, 'name': current.value['name'], 'price': current.value['price']}) # Se ha modificado para la estructura de los datos de la practica
            ordered_list = self._list_in_order(current.right, ordered_list)
        return ordered_list


bst = BST()
bst.insert(10, "Producto A")

