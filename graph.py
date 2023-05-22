from heapq import *

class Graph:
    """
    A class representing a graph using an adjacency list implementation.
    """

    def __init__(self, adj_list):
        """
        Initialize the graph with an adjacency list.

        Args:
            adj_list (dict): The adjacency list representation of the graph.
        """
        self.adj_list = adj_list

    def __str__(self):
        return str(self.adj_list)

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.

        Args:
            vertex: The vertex to add.

        Returns:
            bool: True if the vertex is added successfully, False if it already exists.
        """
        # if not already in graph, add it with empty list
        if vertex in self.adj_list:
            return False
        self.adj_list[vertex] = []
        return True
    
    def add_edge(self, v1, v2, e):
        """
        Add an edge to the graph.

        Args:
            v1: The first vertex of the edge.
            v2: The second vertex of the edge.
            e: The weight or cost associated with the edge.

        Returns:
            bool: True if the edge is added successfully, False if any of the vertices do not exist.
        """
        # if both vertices exist, append each one to eachother
        if v1 in self.adj_list and v2 in self.adj_list:
            temp = (e, v2)
            self.adj_list[v1].append(temp)
            return True
        return False


    def dijkstra(self, start, dest):
        """
        Find the shortest path using Dijkstra's algorithm.

        Args:
            start: The starting node.
            dest: The destination node.

        Returns:
            list: A list containing the shortest path length and the path as nodes.
        """
        q = []
        heappush(q, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}
        path = []
        
        while q:
            current_cost, current_node = heappop(q)
            if current_node == dest:
                break
            
            next_nodes = self.adj_list[current_node]
            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node
                new_cost = cost_visited[current_node] + neigh_cost
                
                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    heappush(q, (new_cost, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = current_node
        
        current_node = dest
        while current_node != start:
            path.append(current_node)
            current_node = visited[current_node]
        path.append(current_node)
        return [current_cost, path[::-1]]


    def bellman_ford(self, source, target):
        """
        Find the shortest path using the Bellman-Ford algorithm.

        Args:
            source: The source node.
            target: The target node.

        Returns:
            list: A list containing the shortest path length and the path as nodes.

        Raises:
            ValueError: If a negative-weight cycle is detected in the graph.
        """
        # initialization
        distances = {node: float('inf') for node in self.adj_list}
        distances[source] = 0
        predecessors = {node: None for node in self.adj_list}

        # relaxation
        for _ in range(len(self.adj_list) - 1):
            for node in self.adj_list:
                for weight, neighbor in self.adj_list[node]:
                    if distances[node] + weight < distances[neighbor]:
                        distances[neighbor] = distances[node] + weight
                        predecessors[neighbor] = node

        # check for negative cycles
        for node in self.adj_list:
            for weight, neighbor in self.adj_list[node]:
                if distances[node] + weight < distances[neighbor]:
                    raise ValueError("Graph contains a negative-weight cycle")

        # Step 4: Retrieve shortest path
        path = []
        current_node = target
        while current_node is not None:
            path.insert(0, current_node)
            current_node = predecessors[current_node]
        length = distances[target]
        return [length, path]
    

    # can't use astar for my project as no heuristic can be provided for non-real world graph
    @staticmethod
    def heuristic(self, node, target): 
        # Custom heuristic function
        return 0


    def astar(self, source, target):
        """
        Find the shortest path using the A* algorithm.

        Args:
            source: The source node.
            target: The target node.

        Returns:
            list: A list containing the shortest path length and the path as nodes.

        Raises:
            ValueError: If no path is found between the source and target nodes.
        """
        # initialization
        open_set = [(0, source)]  # Priority queue of nodes to be explored
        g_scores = {node: float('inf') for node in self.adj_list}  # Cost from start node to current node
        g_scores[source] = 0
        f_scores = {node: float('inf') for node in self.adj_list}  # Estimated total cost from start to target through current node
        f_scores[source] = self.heuristic(source, target)
        came_from = {}  # Store the previous node in the optimal path

        # explore nodes
        while open_set:
            _, current = heappop(open_set)

            if current == target:
                # Reached the target node, reconstruct the path and return
                path = []
                while current in came_from:
                    path.insert(0, current)
                    current = came_from[current]
                path.insert(0, source)
                length = g_scores[target]
                return [length, path]

            for weight, neighbor in self.adj_list[current]:
                # calculate the tentative g-score for the neighbor node
                tentative_g_score = g_scores[current] + weight

                if tentative_g_score < g_scores[neighbor]:
                    # update the optimal path for the neighbor node
                    came_from[neighbor] = current
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = tentative_g_score + self.heuristic(neighbor, target)

                    # add the neighbor to the open set for exploration
                    heappush(open_set, (f_scores[neighbor], neighbor))

        # if the open set is empty and we haven't reached the target node, no path exists
        raise ValueError("No path found between the source and target nodes")

