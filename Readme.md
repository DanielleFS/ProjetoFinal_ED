**Sistema de Triagem e Atendimento (STA)**

**Descrição:**
O STA é um sistema em Python para gerenciar a triagem e atendimento de pacientes em clínicas ou hospitais.
Ele organiza os pacientes em filas normal e prioritária, garantindo que casos mais urgentes ou idosos sejam atendidos primeiro.
Além disso, oferece funcionalidades de controle, relatórios e histórico de chamadas.

**Funcionalidades:**
- Registro de pacientes com nome, idade e nível de urgência.

**Classificação automática:**
- Fila prioritária: urgência > 2 ou idade ≥ 60.
- Fila normal: demais casos.

**Chamada de pacientes:**
- Prioriza fila de urgência antes da normal.

- Desfazer última chamada.

**Painel de espera:**
- Mostra próximo paciente de cada fila.
- Exibe total de pacientes aguardando.

**Relatório de atendimentos:**
- Ordenado por idade usando Heapsort.

- Registro em log de todas as ações realizadas.

**Estruturas utilizadas**
Fila Convencional (deque) → para pacientes normais.

Max-Heap → para fila de prioridade.

Pilha → para histórico de chamadas (desfazer).

Heapsort → para relatórios ordenados por idade.

**Objetivo:**
O sistema busca organizar o fluxo de pacientes, garantindo:

- Atendimento justo e eficiente.
- Priorização de casos graves e idosos.
- Facilidade de gestão com relatórios e logs.