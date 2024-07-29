"""
Esse código já existe dentro do próprio NetSquid, entretanto,
para facilitar o entendimento, decidi reescreve-lo aqui com 
comentários em português e alguns nomes de variáveis trocadas
em busca de melhorar o entendimento do código e aproxima-lo 
do usuário brasileiro.

Outrossim, caso ache preferível, é totalmente possível utilizar
o código original que está dentro do simulador se assim achar melhor.
"""


from netsquid.nodes import Network, Node
from netsquid.examples.teleportation import create_processor, ClassicalConnection, EntanglingConnection

def networkSetup(node_distance: float = 4e-3, depolarization_rate: float = 1e7, dephasing_rate: float = 0.2) -> Network:
    """Cria os componentes físicos de uma conexão quântica
    
    Parâmetros
    ----------
    node_distance : float, opicional
        Distãncia entre os nós
    depolarization_rate : float, opicional
        Taxa de despolarização dos qubits na memória
    dephasing_rate : float, opicional
        Taxa de defasagem das instruções de medição física

    Return
    ------
    :class:`~netsquid.nodes.node.Network`
        Uma rede com os nós "Alice" e "Bob"
        conectados por um entrelaçamento quântico e uma conexão clássica
    
    """
    # Cria os nó iniciais
    alice = Node("Alice", qmemory=create_processor(depolarization_rate, dephasing_rate))
    bob = Node("Bob", qmemory=create_processor(depolarization_rate, dephasing_rate))
    # Cria a rede
    network = Network("Teleportation_network")
    network.add_nodes([alice, bob])
    # Criando uma coneção clássica entre os nós
    classical_connection  = ClassicalConnection(length=node_distance)
    network.add_connection(alice, bob, connection=classical_connection, label="Classical", port_name_node1="cout_bob", port_name_node2="cin_alice")
    # Criando um canal de comunicação quântico
    source_frequency = 4e4 / node_distance
    quantum_connection = EntanglingConnection(length=node_distance, source_frequency=source_frequency)
    # Criando as portas de conexão
    port_ac, port_bc = network.add_connection(alice, bob, connection=quantum_connection, label="quantum", port_name_node1="qin_charlie", port_name_node2="qin_charlie")
    alice.ports[port_ac].forward_input(alice.qmemory.ports['qin1'])
    bob.ports[port_bc].forward_input(bob.qmemory.ports['qin0'])
    return network

