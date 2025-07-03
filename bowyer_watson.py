import numpy as np
from typing import List, Tuple, Set
import math

class Triangle:
    def __init__(self, p1, p2, p3):
        self.vertices = [p1, p2, p3]
        self.circumcenter, self.circumradius = self.calculate_circumcircle()
    
    def calculate_circumcircle(self):
        p1, p2, p3 = self.vertices
        
        # Współrzędne wierzchołków
        ax, ay = p1[0], p1[1]
        bx, by = p2[0], p2[1]
        cx, cy = p3[0], p3[1]
        
        # Obliczenie wyznacznika
        D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        
        if abs(D) < 1e-10:  # Punkty współliniowe
            return np.array([0, 0]), float('inf')
        
        # Środek okręgu opisanego
        ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + 
              (cx**2 + cy**2) * (ay - by)) / D
        uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + 
              (cx**2 + cy**2) * (bx - ax)) / D
        
        circumcenter = np.array([ux, uy])
        
        # Promień okręgu opisanego
        circumradius = np.linalg.norm(p1 - circumcenter)
        
        return circumcenter, circumradius
    
    def contains_in_circumcircle(self, point):
        distance = np.linalg.norm(point - self.circumcenter)
        return distance <= self.circumradius + 1e-10  # Tolerancja numeryczna
    
    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        # Porównujemy zbiory wierzchołków
        return set(map(tuple, self.vertices)) == set(map(tuple, other.vertices))
    
    def __hash__(self):
        return hash(frozenset(map(tuple, self.vertices)))

class BowyerWatsonTriangulation:
    
    def __init__(self):
        self.triangles = []
    
    def create_super_triangle(self, points):
        # Znalezienie ograniczeń punktów
        min_x = np.min(points[:, 0])
        max_x = np.max(points[:, 0])
        min_y = np.min(points[:, 1])
        max_y = np.max(points[:, 1])
        
        # Margines
        margin = max(max_x - min_x, max_y - min_y) * 0.5
        
        # Wierzchołki super-trójkąta
        p1 = np.array([min_x - margin, min_y - margin])
        p2 = np.array([max_x + margin, min_y - margin])
        p3 = np.array([(min_x + max_x) / 2, max_y + 2 * margin])
        
        return Triangle(p1, p2, p3)
    
    def triangulate(self, points):
        if len(points) < 3:
            return []
        
        # 1. Tworzenie super-trójkąta
        super_triangle = self.create_super_triangle(points)
        self.triangles = [super_triangle]
        
        # 2. Dodawanie punktów pojedynczo
        for point in points:
            # Znajdowanie trójkątów, których okręgi opisane zawierają nowy punkt
            bad_triangles = []
            for triangle in self.triangles:
                if triangle.contains_in_circumcircle(point):
                    bad_triangles.append(triangle)
            
            # Znajdowanie krawędzi wielokąta
            polygon = []
            for i, triangle1 in enumerate(bad_triangles):
                for j in range(3):
                    edge = [triangle1.vertices[j], triangle1.vertices[(j + 1) % 3]]
                    
                    # Sprawdzanie czy krawędź jest współdzielona
                    is_shared = False
                    for k, triangle2 in enumerate(bad_triangles):
                        if i != k:
                            vertices2 = set(map(tuple, triangle2.vertices))
                            if (tuple(edge[0]) in vertices2 and 
                                tuple(edge[1]) in vertices2):
                                is_shared = True
                                break
                    
                    if not is_shared:
                        polygon.append(edge)
            
            # Usuwanie złych trójkątów
            for triangle in bad_triangles:
                self.triangles.remove(triangle)
            
            # Tworzenie nowych trójkątów
            for edge in polygon:
                new_triangle = Triangle(edge[0], edge[1], point)
                self.triangles.append(new_triangle)
        
        # 3. Usuwanie trójkątów zawierających wierzchołki super-trójkąta
        super_vertices = set(map(tuple, super_triangle.vertices))
        final_triangles = []
        
        for triangle in self.triangles:
            contains_super_vertex = False
            for vertex in triangle.vertices:
                if tuple(vertex) in super_vertices:
                    contains_super_vertex = True
                    break
            
            if not contains_super_vertex:
                final_triangles.append(triangle.vertices)
        
        return final_triangles
    
    def get_edges(self, triangles):
        edges = set()
        for triangle in triangles:
            for i in range(3):
                v1 = tuple(triangle[i])
                v2 = tuple(triangle[(i + 1) % 3])
                # Sortowanie wierzchołków dla unikalności
                edge = tuple(sorted([v1, v2]))
                edges.add(edge)
        return list(edges)