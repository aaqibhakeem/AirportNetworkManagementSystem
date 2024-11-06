import heapq
import networkx as nx
import itertools

class ShortestPathAlgorithms:
    @staticmethod
    def calculate_custom_distance(pos_u, pos_v):
        return (((pos_u[0] - pos_v[0]) * 100) ** 2 + ((pos_u[1] - pos_v[1]) * 110) ** 2) ** 0.5

    @staticmethod
    def compute_shortest_path_dijkstra(G, source, destination):
        def dijkstra(graph, start, end):
            queue = [(0, start, [])]
            seen = set()
            min_dist = {start: 0}
            while queue:
                (cost, node, path) = heapq.heappop(queue)
                if node in seen:
                    continue
                seen.add(node)
                path = path + [node]
                if node == end:
                    return path, cost
                for neighbor in graph.neighbors(node):
                    if neighbor in seen:
                        continue
                    prev_cost = min_dist.get(neighbor, None)
                    new_cost = cost + graph[node][neighbor]['distance']
                    if prev_cost is None or new_cost < prev_cost:
                        min_dist[neighbor] = new_cost
                        heapq.heappush(queue, (new_cost, neighbor, path))
            return None, float('inf')
        return dijkstra(G, source, destination)

    @staticmethod
    def compute_shortest_path_astar(G, source, destination, heuristic_type):
        def astar(graph, start, end, heuristic_func):
            open_set = []
            heapq.heappush(open_set, (0, start))
            came_from = {start: None}
            g_score = {node: float('inf') for node in graph.nodes}
            g_score[start] = 0
            f_score = {node: float('inf') for node in graph.nodes}
            f_score[start] = heuristic_func(start, end)
            
            while open_set:
                _, current = heapq.heappop(open_set)
                if current == end:
                    path = []
                    while current:
                        path.append(current)
                        current = came_from[current]
                    return path[::-1], g_score[end]
                for neighbor in graph.neighbors(current):
                    tentative_g_score = g_score[current] + graph[current][neighbor]['distance']
                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + heuristic_func(neighbor, end)
                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
            return None, float('inf')

        def heuristic(u, v):
            pos_u = G.nodes[u]['pos']
            pos_v = G.nodes[v]['pos']
            if heuristic_type == 'euclidean':
                return ShortestPathAlgorithms.calculate_custom_distance(pos_u, pos_v)
            elif heuristic_type == 'manhattan':
                return abs(pos_u[0] - pos_v[0]) * 100 + abs(pos_u[1] - pos_v[1]) * 110
            elif heuristic_type == 'chebyshev':
                return max(abs(pos_u[0] - pos_v[0]) * 100, abs(pos_u[1] - pos_v[1]) * 110)
            else:
                return 0  
        return astar(G, source, destination, heuristic)

    @staticmethod
    def compute_shortest_path_bellman_ford(G, source, destination):
        def bellman_ford(graph, start, end):
            distance = {node: float('inf') for node in graph.nodes}
            distance[start] = 0
            predecessor = {node: None for node in graph.nodes}
            for _ in range(len(graph.nodes) - 1):
                for u, v, data in graph.edges(data=True):
                    weight = data['distance']
                    if distance[u] + weight < distance[v]:
                        distance[v] = distance[u] + weight
                        predecessor[v] = u
                    if distance[v] + weight < distance[u]:
                        distance[u] = distance[v] + weight
                        predecessor[u] = v
            for u, v, data in graph.edges(data=True):
                weight = data['distance']
                if distance[u] + weight < distance[v]:
                    print("Negative weight cycle detected.")
                    return None, float('inf')
            path = []
            current = end
            while current:
                path.append(current)
                current = predecessor[current]
            path = path[::-1]
            return path, distance[end]

        return bellman_ford(G, source, destination)

    @staticmethod
    def compute_all_shortest_paths(G, source, destination):
        results = {}

        dijkstra_path, dijkstra_distance = ShortestPathAlgorithms.compute_shortest_path_dijkstra(G, source, destination)
        results["Dijkstra"] = (dijkstra_path, dijkstra_distance)
        
        heuristics = ['euclidean', 'manhattan', 'chebyshev']
        astar_results = {}
        
        for heuristic in heuristics:
            path, distance = ShortestPathAlgorithms.compute_shortest_path_astar(G, source, destination, heuristic)
            if path:
                astar_results[heuristic] = (path, distance)
        
        for heuristic in heuristics:
            results[f"A* ({heuristic})"] = astar_results[heuristic]
        
        bellman_ford_path, bellman_ford_distance = ShortestPathAlgorithms.compute_shortest_path_bellman_ford(G, source, destination)
        results["Bellman-Ford"] = (bellman_ford_path, bellman_ford_distance)

        return results

    @staticmethod
    def compute_shortest_path_with_exact_vias(G, source, destination, num_vias):
        all_airports = list(G.nodes())
        all_airports.remove(source)
        all_airports.remove(destination)
        
        possible_via_points = itertools.combinations(all_airports, num_vias)

        shortest_path = None
        shortest_distance = float('inf')

        for via_points in possible_via_points:
            path = [source] + list(via_points) + [destination]
            
            total_distance = 0
            for i in range(len(path) - 1):
                if G.has_edge(path[i], path[i+1]):
                    total_distance += G[path[i]][path[i+1]]['distance']
                else:
                    total_distance = float('inf')

            if total_distance < shortest_distance:
                shortest_distance = total_distance
                shortest_path = path

        return shortest_path, shortest_distance