import re
N_PROJETOS = 50
N_ALUNOS = 200
MAX_VAGAS = 80

class Projeto:
    def __init__(self, codigo, n_vagas, min_notas):
        self.codigo = codigo
        self.n_vagas = n_vagas
        self.min_notas = min_notas
        self.alunos_atribuidos = []

    def __repr__(self):
        return f"Projeto('{self.codigo}', Vagas: {self.n_vagas}, Nota mínima: {self.min_notas}, Alunos: {[aluno.codigo for aluno in self.alunos_atribuidos]})"

class Aluno:
    def __init__(self, codigo, preferencias, nota):
        self.codigo = codigo
        self.preferencias = preferencias
        self.nota = nota
        self.projeto_atribuido = None

    def __repr__(self):
        return f"Aluno('{self.codigo}', Nota: {self.nota}, Prefs: {self.preferencias}, Projeto: {self.projeto_atribuido})"
    

projetos = []
alunos = []

def extrair_e_popular_listas(nome_arquivo, lista_projetos, lista_alunos):
    padrao_projeto = re.compile(r"^\((P\d+), (\d+), (\d+)\)$") 
    padrao_aluno = re.compile(r"^\((A\d+)\):\((.*?)\) \((\d+)\)$")

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                
                if not linha or linha.startswith('//'):
                    continue
                
                match_projeto = padrao_projeto.match(linha)
                if match_projeto:
                    codigo = match_projeto.group(1)
                    n_vagas = int(match_projeto.group(2))
                    min_notas = int(match_projeto.group(3))

                    projeto = Projeto(codigo, n_vagas, min_notas)
                    lista_projetos.append(projeto)
                    continue

                match_aluno = padrao_aluno.match(linha)
                if match_aluno:
                    codigo = match_aluno.group(1)
                    projetos_str = match_aluno.group(2)
                    nota = int(match_aluno.group(3))
                
                    preferencias = [p.strip() for p in projetos_str.split(',')]
                    
                    aluno = Aluno(codigo, preferencias, nota)
                    lista_alunos.append(aluno)
                    continue
    except Exception as e:
        print(e)


def SPA_GaleShapley(projetos, alunos):
    c = 0
    alunos_livres = list(alunos)
    projetos_map = {p.codigo: p for p in projetos}
    while alunos_livres:
        aluno = alunos_livres.pop(0)

        if aluno.preferencias:
            projeto_codigo = aluno.preferencias.pop(0)
            projeto = projetos_map.get(projeto_codigo)
            if projeto and aluno.nota >= projeto.min_notas:
                if len(projeto.alunos_atribuidos) < projeto.n_vagas:
                    projeto.alunos_atribuidos.append(aluno)
                    aluno.projeto_atribuido = projeto
                
                else:
                    pior_aluno = min(projeto.alunos_atribuidos, key=lambda a: a.nota)
                    
                    if aluno.nota > pior_aluno.nota:
                        projeto.alunos_atribuidos.remove(pior_aluno)
                        pior_aluno.projeto_atribuido = None
                        alunos_livres.append(pior_aluno)
   
                        projeto.alunos_atribuidos.append(aluno)
                        aluno.projeto_atribuido = projeto
                    

            if aluno.projeto_atribuido is None:
                alunos_livres.append(aluno)

    return projetos, alunos

    

extrair_e_popular_listas('entradaProj2.25TAG.txt', projetos, alunos)
projetos, alunos = SPA_GaleShapley(projetos, alunos)
print(alunos)

