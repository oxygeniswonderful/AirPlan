from Algoritms.DijkstraNodeDecorator import DijkstraNodeDecorator
from Algoritms.MinHeap import MinHeap
from Algoritms.Node import Node


class Graph:

    def __init__(self, nodes):

        self.adj_list = [[node, []] for node in nodes]
        for i in range(len(nodes)):
            nodes[i].index = i

    def connect_dir(self, node1, node2, weight):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        # Отмечает, что нижеуказанное не предотвращает от добавления связи дважды
        self.adj_list[node1][1].append((node2, weight))

    def connect(self, node1, node2, weight):
        self.connect_dir(node1, node2, weight)
        self.connect_dir(node2, node1, weight)

    def connections(self, node):
        node = self.get_index_from_node(node)
        return self.adj_list[node][1]

    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index

    def dijkstra(self, src):

        src_index = self.get_index_from_node(src)
        # Указывает узлы к DijkstraNodeDecorators
        # Это инициализирует все предварительные расстояния до бесконечности
        dnodes = [DijkstraNodeDecorator(node_edges[0]) for node_edges in self.adj_list]
        # Устанавливает предварительное расстояние исходного узла до 0 и его массив перескоков к его узлу
        dnodes[src_index].prov_dist = 0
        dnodes[src_index].hops.append(dnodes[src_index].node)
        # Устанавливает все методы настройки кучи
        is_less_than = lambda a, b: a.prov_dist < b.prov_dist
        get_index = lambda node: node.index()
        update_node = lambda node, data: node.update_data(data)

        # Подтверждает работу кучи с DijkstraNodeDecorators с узлами
        heap = MinHeap(dnodes, is_less_than, get_index, update_node)

        min_dist_list = []

        while heap.size() > 0:
            # Получает узел кучи, что еще не просматривался ('seen')
            # и находится на минимальном расстоянии от исходного узла
            min_decorated_node = heap.pop()
            min_dist = min_decorated_node.prov_dist
            hops = min_decorated_node.hops
            min_dist_list.append([min_dist, hops])

            # Получает все следующие перескоки. Это больше не O(n^2) операция
            connections = self.connections(min_decorated_node.node)
            # Для каждой связи обновляет ее путь и полное расстояние от
            # исходного узла, если общее расстояние меньше, чем текущее расстояние
            # в массиве dist
            for (inode, weight) in connections:
                node = self.adj_list[inode][0]
                heap_location = heap.order_mapping[inode]
                if (heap_location is not None):
                    tot_dist = weight + min_dist
                    if tot_dist < heap.nodes[heap_location].prov_dist:
                        hops_cpy = list(hops)
                        hops_cpy.append(node)
                        data = {'prov_dist': tot_dist, 'hops': hops_cpy}
                        heap.decrease_key(heap_location, data)

        return min_dist_list

    def path_from_to(self, from_nod, to_ind):

        l = ([(weight, [n.data for n in node]) for (weight, node) in self.dijkstra(from_nod)])
        path = []
        w = []
        for ob in l:
            if len(ob[1]) > 0:
                if ob[1][len(ob[1]) - 1] == to_ind:
                    # print(l)
                    path = ob[1]
                    w = ob[0]
        ans = [w, path]
        return ans