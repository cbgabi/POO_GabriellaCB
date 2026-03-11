from abc import ABC, abstractmethod

class LimiteEmprestimosExcedido(Exception):
    pass

class LivroIndisponivel(Exception):
    pass


class Livro:
    def __init__(self, isbn, titulo, autor):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.disponivel = True

    def emprestar(self):
        if not self.disponivel:
            raise LivroIndisponivel("Livro indisponivel para emprestimo.")
        self.disponivel = False

    def devolver(self):
        self.disponivel = True


class Usuario(ABC):
    def __init__(self, matricula, nome):
        self.matricula = matricula
        self.nome = nome
        self.lista_livros_emprestados = []

    @abstractmethod
    def pegar_emprestado(self, livro):
        pass

    @abstractmethod
    def devolver_livro(self, livro):
        pass


class Aluno(Usuario):
    LIMITE = 3

    def pegar_emprestado(self, livro):
        if len(self.lista_livros_emprestados) >= self.LIMITE:
            raise LimiteEmprestimosExcedido("Aluno excedeu o limite de emprestimos.")
        livro.emprestar()
        self.lista_livros_emprestados.append(livro)

    def devolver_livro(self, livro):
        if livro in self.lista_livros_emprestados:
            self.lista_livros_emprestados.remove(livro)
            livro.devolver()


class Professor(Usuario):
    LIMITE = 5

    def pegar_emprestado(self, livro):
        if len(self.lista_livros_emprestados) >= self.LIMITE:
            raise LimiteEmprestimosExcedido("Professor excedeu o limite de emprestimos.")
        livro.emprestar()
        self.lista_livros_emprestados.append(livro)

    def devolver_livro(self, livro):
        if livro in self.lista_livros_emprestados:
            self.lista_livros_emprestados.remove(livro)
            livro.devolver()


class Biblioteca:
    def __init__(self):
        self.acervo = []
        self.usuarios_cadastrados = []

    def cadastrar_usuario(self, usuario):
        self.usuarios_cadastrados.append(usuario)

    def adicionar_livro(self, livro):
        self.acervo.append(livro)

    def registrar_emprestimo(self, matricula, isbn):
        usuario = None
        livro = None

        for u in self.usuarios_cadastrados:
            if u.matricula == matricula:
                usuario = u

        for l in self.acervo:
            if l.isbn == isbn:
                livro = l

        if usuario and livro:
            usuario.pegar_emprestado(livro)

    def consultar_livros_emprestados(self):
        for usuario in self.usuarios_cadastrados:
            print(f"\nUsuário: {usuario.nome}")
            for livro in usuario.lista_livros_emprestados:
                print(f"- {livro.titulo}")


biblioteca = Biblioteca()

l1 = Livro("LIV001", "Titulo 1", "Autor 1")
l2 = Livro("LIV002", "Titulo 2", "Autor 2")
l3 = Livro("LIV003", "Titulo 3", "Autor 3")

biblioteca.adicionar_livro(l1)
biblioteca.adicionar_livro(l2)
biblioteca.adicionar_livro(l3)

aluno = Aluno("A001", "chris")
prof = Professor("P001", "Dr. Oto")

biblioteca.cadastrar_usuario(aluno)
biblioteca.cadastrar_usuario(prof)

biblioteca.registrar_emprestimo("A001", "LIV001")
biblioteca.registrar_emprestimo("P001", "LIV002")

biblioteca.consultar_livros_emprestados()