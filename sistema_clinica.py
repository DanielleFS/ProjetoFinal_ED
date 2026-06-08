# 1. Entidade Básica: O Paciente #

import time
from collections import deque

class Paciente:
    def __init__(self, id_paciente, nome, idade, nivel_urgencia):
        self.id_paciente = id_paciente
        self.nome = nome
        self.idade = idade
        self.nivel_urgencia = nivel_urgencia
        self.timestamp_chegada = time.time()
        
        # Define automaticamente a origem com base na regra de negócio
        if self.nivel_urgencia > 2 or self.idade >= 60:
            self.origem_fila = 'prioridade'
        else:
            self.origem_fila = 'normal'

    def __repr__(self):
        return f"[ID:{self.id_paciente}] {self.nome} | Idade: {self.idade} | Urgência: {self.nivel_urgencia}"

# 2. Estruturas Lineares: Fila e Pilha #

class FilaConvencional:
    def __init__(self):
        self.fila = deque()

    def enfileirar(self, paciente):
        self.fila.append(paciente)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.fila.popleft()
        return None

    def esta_vazia(self):
        return len(self.fila) == 0

class PilhaChamadas:
    def __init__(self):
        self.pilha = []

    def push(self, paciente):
        self.pilha.append(paciente)

    def pop(self):
        if not self.esta_vazia():
            return self.pilha.pop()
        return None

    def esta_vazia(self):
        return len(self.pilha) == 0

# 3. O Coração do Projeto: Max-Heap (Fila de Prioridade) #

class MaxHeap:
    def __init__(self):
        self.heap = []

    def _pai(self, i): return (i - 1) // 2
    def _filho_esq(self, i): return 2 * i + 1
    def _filho_dir(self, i): return 2 * i + 2

    def _tem_prioridade(self, p1, p2):
        """Define quem deve ser atendido primeiro (Critérios de desempate)"""
        if p1.nivel_urgencia != p2.nivel_urgencia:
            return p1.nivel_urgencia > p2.nivel_urgencia # Maior urgência ganha
        if p1.idade != p2.idade:
            return p1.idade > p2.idade # Se empatar na urgência, mais velho ganha
        return p1.timestamp_chegada < p2.timestamp_chegada # Se empatar, quem chegou antes

    def inserir(self, paciente):
        """Insere no final e sobe na árvore (O(log n))"""
        self.heap.append(paciente)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        pai = self._pai(i)
        if i > 0 and self._tem_prioridade(self.heap[i], self.heap[pai]):
            # Faz a troca (swap)
            self.heap[i], self.heap[pai] = self.heap[pai], self.heap[i]
            self._heapify_up(pai)

    def extrair_max(self):
        """Remove a raiz (maior prioridade), joga o último nó pra raiz e desce na árvore (O(log n))"""
        if self.esta_vazia():
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        raiz = self.heap[0]
        self.heap[0] = self.heap.pop() # Move o último nó para a raiz
        self._heapify_down(0)
        return raiz

    def _heapify_down(self, i):
        maior = i
        esq = self._filho_esq(i)
        dir = self._filho_dir(i)
        n = len(self.heap)

        if esq < n and self._tem_prioridade(self.heap[esq], self.heap[maior]):
            maior = esq
        if dir < n and self._tem_prioridade(self.heap[dir], self.heap[maior]):
            maior = dir

        if maior != i:
            self.heap[i], self.heap[maior] = self.heap[maior], self.heap[i]
            self._heapify_down(maior)

    def esta_vazia(self):
        return len(self.heap) == 0

# 4. Algoritmo Heapsort (Para Relatórios) #

def heapsort_por_idade(lista_pacientes):
    """Ordena in-place a lista de pacientes por idade de forma crescente (O(n log n))"""
    n = len(lista_pacientes)

    def heapify(arr, n, i):
        maior = i
        esq = 2 * i + 1
        dir = 2 * i + 2

        if esq < n and arr[esq].idade > arr[maior].idade:
            maior = esq
        if dir < n and arr[dir].idade > arr[maior].idade:
            maior = dir

        if maior != i:
            arr[i], arr[maior] = arr[maior], arr[i]
            heapify(arr, n, maior)

    # 1. Constrói o Max-Heap inicial
    for i in range(n // 2 - 1, -1, -1):
        heapify(lista_pacientes, n, i)

    # 2. Extrai os elementos um a um da raiz
    for i in range(n - 1, 0, -1):
        lista_pacientes[i], lista_pacientes[0] = lista_pacientes[0], lista_pacientes[i]
        heapify(lista_pacientes, i, 0)

# 5. O Controlador do Sistema (Regras de Negócio) #

class SistemaAtendimento:
    def __init__(self):
        self.fila_normal = FilaConvencional()
        self.fila_prioritaria = MaxHeap()
        self.historico_desfazer = PilhaChamadas()
        self.pacientes_atendidos = [] # Para usar com o Heapsort depois
        self.contador_ids = 1
        self.nome_arquivo_log = "log_"+ str(int(time.time()))+".txt"

    def registrar_chegada(self, nome, idade, nivel_urgencia):
        paciente = Paciente(self.contador_ids, nome, idade, nivel_urgencia)
        self.contador_ids += 1
        
        if paciente.origem_fila == 'prioridade':
            self.fila_prioritaria.inserir(paciente)
            print(f"-> {paciente.nome} encaminhado(a) para Fila de PRIORIDADE.")
        else:
            self.fila_normal.enfileirar(paciente)
            print(f"-> {paciente.nome} encaminhado(a) para Fila NORMAL.")

        self.log_txt("Registrado o paciente: " + repr(paciente))

    def chamar_proximo(self):
        # Regra: Esgota a prioridade primeiro. Se não houver, chama normal.
        if not self.fila_prioritaria.esta_vazia():
            paciente_chamado = self.fila_prioritaria.extrair_max()
        elif not self.fila_normal.esta_vazia():
            paciente_chamado = self.fila_normal.desenfileirar()
        else:
            print("Não há pacientes na sala de espera.")
            return None

        # Joga na pilha para permitir o "Ctrl+Z"
        self.historico_desfazer.push(paciente_chamado)
        self.pacientes_atendidos.append(paciente_chamado) # Salva para o relatório
        print(f"\n[CHAMADA] Consultório 1: {paciente_chamado.nome}")

        self.log_txt("Próximo paciente para atendimento: " + repr(paciente_chamado))

        return paciente_chamado
    

    def desfazer_ultima_chamada(self):
        paciente_cancelado = self.historico_desfazer.pop()
        if not paciente_cancelado:
            print("Não há atendimento para desfazer.")
            self.log_txt("Não há atendimento para desfazer.")
            return
            
        # Remove do log de atendidos
        if paciente_cancelado in self.pacientes_atendidos:
            self.pacientes_atendidos.remove(paciente_cancelado)

        # Devolve para a estrutura original correta
        if paciente_cancelado.origem_fila == 'prioridade':
            self.fila_prioritaria.inserir(paciente_cancelado)
        else:
            self.fila_normal.enfileirar(paciente_cancelado)
            
        print(f"-> Chamada cancelada. {paciente_cancelado.nome} retornou à fila de espera.")

        self.log_txt("Atendimento cancelado para o paciente: " + repr(paciente_cancelado))

    def log_txt(self,log):
        with open(self.nome_arquivo_log, "a", encoding="utf-8") as f:
            f.write(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()) +"   "+log+"\n")

# Menu Interativo em console #

def exibir_menu():
    print("\n" + "="*45)
    print("   SISTEMA DE TRIAGEM E ATENDIMENTO (STAC)   ")
    print("="*45)
    print("1. Registrar chegada de paciente")
    print("2. Chamar próximo paciente")
    print("3. Desfazer última chamada (Ctrl+Z)")
    print("4. Visualizar painel de espera")
    print("5. Relatório de atendimentos") #(Heapsort)
    print("0. Sair do sistema")
    print("="*45)

def main():
    sistema = SistemaAtendimento()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        # sistema.log_txt("A opção selecionada foi: "+ opcao)

        if opcao == '1':
            print("\n--- REGISTRAR NOVO PACIENTE ---")
            nome = input("Nome do paciente: ")
            
            # Tratamento de erro para garantir que o usuário digite números
            try:
                idade = int(input("Idade: "))
                urgencia = int(input("Nível de Urgência (1 a 5, onde 5 é mais grave): "))
                if urgencia < 1 or urgencia > 5:
                    print("Atenção: Nível de urgência deve ser entre 1 e 5. Padrão (1) aplicado.")
                    urgencia = 1
                
                sistema.registrar_chegada(nome, idade, urgencia)
                
            except ValueError:
                print("\n[ERRO] Idade e Urgência devem ser números inteiros! Cadastro cancelado.")

        elif opcao == '2':
            print("\n--- CHAMANDO PACIENTE ---")
            sistema.chamar_proximo()

        elif opcao == '3':
            print("\n--- DESFAZER CHAMADA ---")
            sistema.desfazer_ultima_chamada()

        elif opcao == '4':
            print("\n--- PAINEL DE ESPERA ---")
            # Espiando (Peek) as estruturas sem remover
            prox_prioridade = sistema.fila_prioritaria.heap[0] if not sistema.fila_prioritaria.esta_vazia() else None
            prox_normal = sistema.fila_normal.fila[0] if not sistema.fila_normal.esta_vazia() else None
            
            print(f"Próximo da Prioridade: {prox_prioridade if prox_prioridade else 'Nenhum'}")
            print(f"Próximo da Fila Normal: {prox_normal if prox_normal else 'Nenhum'}")
            
            total_espera = len(sistema.fila_prioritaria.heap) + len(sistema.fila_normal.fila)
            print(f"Total de pacientes aguardando: {total_espera}")

            sistema.log_txt("Vizualizado o painel de espera.")

        elif opcao == '5':
            print("\n--- RELATÓRIO DE ATENDIDOS (Ordenado por Idade) ---")
            if not sistema.pacientes_atendidos:
                print("Nenhum paciente finalizou o atendimento ainda.")
            else:
                # Criamos uma cópia para não alterar a ordem original do histórico
                lista_relatorio = sistema.pacientes_atendidos.copy()
                
                # Aplica o Heapsort desenvolvido na etapa anterior
                heapsort_por_idade(lista_relatorio)
                
                print(f"Total de atendimentos: {len(lista_relatorio)}")
                for p in lista_relatorio:
                    print(f"- {p.nome} (Idade: {p.idade} | Urgência: {p.nivel_urgencia})")

            sistema.log_txt("Vizualizado o relatório de atendimentos.")


        elif opcao == '0':
            print("\nEncerrando o sistema. Até logo!")
            sistema.log_txt("Sistema encerrado.")

            break

        else:
            print("\n[ERRO] Opção inválida. Tente novamente.")
            sistema.log_txt("Opção inválida selecionada.")
            
        # Uma pequena pausa para o usuário ler as mensagens antes de exibir o menu novamente
        input("\nPressione ENTER para continuar...")

# Ponto de entrada do script
if __name__ == "__main__":
    main()
