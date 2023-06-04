N = 4  # Orden del árbol B*

class Nodo:
    def __init__(self, hoja=False):
        self.hoja = hoja
        self.claves = []
        self.hijos = []

    def insertar(self, clave):
        if not self.claves:
            self.claves.append(clave)
            return self

        if clave < self.claves[0]:
            self.claves.insert(0, clave)
            return self

        if clave > self.claves[-1]:
            self.claves.append(clave)
            return self

        for i in range(len(self.claves) - 1):
            if self.claves[i] < clave < self.claves[i + 1]:
                self.claves.insert(i + 1, clave)
                return self

    def encontrar(self, clave):
        if clave in self.claves:
            return self
        elif self.hoja:
            return None

        for i in range(len(self.claves)):
            if clave < self.claves[i]:
                return self.hijos[i].encontrar(clave)

        return self.hijos[-1].encontrar(clave)

    def imprimir_arbol(self, nivel=0):
        if self.hoja:
            print("Nodo Hoja:", self.claves)
        else:
            print("Nivel", nivel, "Nodo:", self.claves)
            for hijo in self.hijos:
                hijo.imprimir_arbol(nivel + 1)

class ArbolBStar:
    def __init__(self):
        self.raiz = Nodo(hoja=True)

    def insertar(self, clave):
        nodo = self.raiz
        if len(nodo.claves) == (N - 1):
            nueva_raiz = Nodo()
            nueva_raiz.hijos.append(nodo)
            self.raiz = nueva_raiz
            nueva_raiz.insertar(clave)
        else:
            nodo.insertar(clave)

    def encontrar(self, clave):
        return self.raiz.encontrar(clave)

    def imprimir_arbol(self):
        self.raiz.imprimir_arbol()

    def buscar(self, clave):
        resultado = self.encontrar(clave)
        if resultado:
            print("¡Clave encontrada!")
        else:
            print("¡Clave no encontrada!")

# Prueba la implementación del árbol B*
arbol_bstar = ArbolBStar()
arbol_bstar.insertar(3)
arbol_bstar.insertar(7)
arbol_bstar.insertar(9)
arbol_bstar.insertar(11)
arbol_bstar.insertar(2)
arbol_bstar.insertar(4)
arbol_bstar.insertar(6)
arbol_bstar.insertar(8)
arbol_bstar.insertar(10)
arbol_bstar.insertar(12)

arbol_bstar.imprimir_arbol()

arbol_bstar.buscar(6)
arbol_bstar.buscar(13)
