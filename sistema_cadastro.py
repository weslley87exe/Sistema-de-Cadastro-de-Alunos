import json
import os
from typing import List, Dict, Optional

# Tipo pra deixar claro o que é um aluno
Aluno = Dict[str, object]

class SistemaCadastro:
    def __init__(self, arquivo: str = "alunos.json"):
        self.arquivo = arquivo
        self.alunos: List[Aluno] = []
        self.carrega_dados()

    def carrega_dados(self) -> None:
        """Carrega alunos do arquivo JSON, se existir."""
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                self.alunos = json.load(f)
        else:
            self.alunos = []

    def salva_dados(self) -> None:
        """Salva alunos no arquivo JSON."""
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.alunos, f, ensure_ascii=False, indent=4)

    def cadastrar_aluno(self, nome: str, matricula: str, idade: int, nota: float) -> bool:
        """Cadastra aluno se matrícula não existir. Retorna True se sucesso."""
        if any(a['matricula'] == matricula for a in self.alunos):
            return False
        self.alunos.append({
            "nome": nome,
            "matricula": matricula,
            "idade": idade,
            "nota": nota
        })
        self.salva_dados()
        return True

    def listar_alunos(self) -> List[str]:
        """Retorna lista formatada de alunos."""
        if not self.alunos:
            return []
        return [f"{i+1}. Nome: {a['nome']} | Idade: {a['idade']} anos | Matrícula: {a['matricula']} | Nota: {a['nota']:.2f}"
                for i, a in enumerate(self.alunos)]

    def encontrar_aluno(self, matricula: str) -> Optional[Aluno]:
        """Encontra aluno pela matrícula."""
        return next((a for a in self.alunos if a['matricula'] == matricula), None)

    def editar_aluno(self, matricula: str, novo_nome: Optional[str], nova_idade: Optional[int], nova_nota: Optional[float]) -> bool:
        """Edita dados do aluno com a matrícula. Retorna True se encontrado e editado."""
        aluno = self.encontrar_aluno(matricula)
        if not aluno:
            return False
        if novo_nome:
            aluno["nome"] = novo_nome
        if nova_idade is not None:
            aluno["idade"] = nova_idade
        if nova_nota is not None:
            aluno["nota"] = nova_nota
        self.salva_dados()
        return True

    def remover_aluno(self, matricula: str) -> bool:
        """Remove aluno pela matrícula. Retorna True se removido."""
        aluno = self.encontrar_aluno(matricula)
        if not aluno:
            return False
        self.alunos.remove(aluno)
        self.salva_dados()
        return True

def main():
    sistema = SistemaCadastro()

    while True:
        print("\n--- MENU ---")
        print("1. Cadastrar aluno")
        print("2. Listar alunos")
        print("3. Editar aluno")
        print("4. Remover aluno")
        print("5. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome: ").strip()
            matricula = input("Matrícula: ").strip()
            try:
                idade = int(input("Idade: ").strip())
                nota = float(input("Nota: ").replace(",", ".").strip())
            except ValueError:
                print("❌ Entrada inválida para idade ou nota.")
                continue
            if sistema.cadastrar_aluno(nome, matricula, idade, nota):
                print(f"✅ Aluno '{nome}' cadastrado com sucesso!")
            else:
                print("❌ Matrícula já cadastrada.")

        elif opcao == "2":
            lista = sistema.listar_alunos()
            if not lista:
                print("📭 Nenhum aluno cadastrado.")
            else:
                print("\n--- LISTA DE ALUNOS ---")
                for linha in lista:
                    print(linha)

        elif opcao == "3":
            matricula = input("Digite a matrícula do aluno que deseja editar: ").strip()
            aluno = sistema.encontrar_aluno(matricula)
            if not aluno:
                print("❌ Matrícula não encontrada.")
                continue

            novo_nome = input(f"Novo nome ({aluno['nome']}): ").strip() or None
            nova_idade_str = input(f"Nova idade ({aluno['idade']}): ").strip()
            nova_idade = int(nova_idade_str) if nova_idade_str.isdigit() else None
            nova_nota_str = input(f"Nova nota ({aluno['nota']}): ").strip()
            try:
                nova_nota = float(nova_nota_str.replace(",", ".")) if nova_nota_str else None
            except ValueError:
                nova_nota = None

            if sistema.editar_aluno(matricula, novo_nome, nova_idade, nova_nota):
                print("✅ Dados atualizados com sucesso!")
            else:
                print("❌ Falha ao atualizar dados.")

        elif opcao == "4":
            matricula = input("Digite a matrícula do aluno que deseja remover: ").strip()
            aluno = sistema.encontrar_aluno(matricula)
            if not aluno:
                print("❌ Matrícula não encontrada.")
                continue
            confirmar = input(f"Tem certeza que deseja remover '{aluno['nome']}'? (s/n): ").lower()
            if confirmar == "s":
                if sistema.remover_aluno(matricula):
                    print("🗑️ Aluno removido com sucesso!")
                else:
                    print("❌ Falha ao remover aluno.")
            else:
                print("❌ Operação cancelada.")

        elif opcao == "5":
            print("Saindo... 👋")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
