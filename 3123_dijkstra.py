import numpy as np

class Solution:
    def graph(self, edges, n):
        children = {i : set() for i in range(n)}
        weights = {}

        for a, b, w in edges:
            children[a].add(b)
            children[b].add(a)
        
            weights[(a, b)] = w
            weights[(b, a)] = w

        return children, weights
    

    def dijkstra(self, edges, s, n):
        children, weights = self.graph(edges, n)
        distances = {i : np.inf for i in range(n)}
        distances[s] = 0
        dist_to_nodes = {np.inf : set([i for i in range(n) if i != s])}
        dist_to_nodes[0] = {s}

        hp = [0]
        heapq.heapify(hp)
        visited = set()

        while hp:
            dist = heapq.heappop(hp)
            if dist == np.inf:
                return distances

            if dist_to_nodes[dist]:
                for el in dist_to_nodes[dist]:
                    curr_node = el
                    dist_to_nodes[dist].remove(el)
                    break

                visited.add(curr_node)

                for child in children[curr_node]:
                    if child not in visited:
                        old_dist = distances[child]
                        new_dist = min(old_dist, dist + weights[(curr_node, child)])
                        heapq.heappush(hp, new_dist)

                        dist_to_nodes[old_dist].remove(child)
                        dist_to_nodes[new_dist] = dist_to_nodes.get(new_dist, set())
                        dist_to_nodes[new_dist].add(child)
                        
                        distances[child] = new_dist
    
        return distances
                    
        
    def findAnswer(self, n: int, edges: List[List[int]]) -> List[bool]:
        s_distances = self.dijkstra(edges, 0, n)
        t_distances = self.dijkstra(edges, n - 1, n)
        answer = [False] * len(edges)

        dist = s_distances[n - 1]

        if dist == np.inf:
            return answer

        for ind, edge in enumerate(edges):
            a, b, w = edge
            if s_distances[a] + t_distances[b] + w == dist or s_distances[b] + t_distances[a] + w == dist:
                answer[ind] = True
        
        return answer
        
