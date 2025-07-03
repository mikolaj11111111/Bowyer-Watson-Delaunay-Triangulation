
import numpy as np
from typing import Dict, List
import math

class TriangulationStatistics:
    
    def calculate_triangle_quality(self, vertices):

        p1, p2, p3 = vertices
        
        # Długości boków
        a = np.linalg.norm(p2 - p3)
        b = np.linalg.norm(p1 - p3)
        c = np.linalg.norm(p1 - p2)
        
        # Półobwód
        s = (a + b + c) / 2
        
        # Pole trójkąta (wzór Herona)
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        
        # Promień okręgu wpisanego
        inradius = area / s
        
        # Promień okręgu opisanego
        circumradius = (a * b * c) / (4 * area)
        
        # Jakość kształtu (stosunek promieni)
        quality = inradius / circumradius if circumradius > 0 else 0
        
        # Normalizacja do przedziału [0, 1], gdzie 1 to trójkąt równoboczny
        normalized_quality = 2 * quality  # Dla trójkąta równobocznego stosunek = 0.5
        
        return min(normalized_quality, 1.0)
    
    def calculate_triangle_area(self, vertices):
        """Oblicza pole trójkąta"""
        p1, p2, p3 = vertices
        
        # Wzór na pole za pomocą iloczynu wektorowego
        v1 = p2 - p1
        v2 = p3 - p1
        
        area = 0.5 * abs(np.cross(v1, v2))
        return area
    
    def calculate_angles(self, vertices):
        """Oblicza kąty w trójkącie"""
        p1, p2, p3 = vertices
        
        # Wektory boków
        v1 = p2 - p1
        v2 = p3 - p1
        v3 = p3 - p2
        
        # Długości boków
        a = np.linalg.norm(v3)  # Bok naprzeciwko p1
        b = np.linalg.norm(p3 - p1)  # Bok naprzeciwko p2
        c = np.linalg.norm(v1)  # Bok naprzeciwko p3
        
        # Kąty (w radianach) - prawo cosinusów
        angle1 = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1, 1))
        angle2 = np.arccos(np.clip((a**2 + c**2 - b**2) / (2 * a * c), -1, 1))
        angle3 = np.arccos(np.clip((a**2 + b**2 - c**2) / (2 * a * b), -1, 1))
        
        return np.degrees([angle1, angle2, angle3])
    
    def calculate_statistics(self, points, simplices):
        statistics = {
            'num_triangles': len(simplices),
            'quality_values': [],
            'areas': [],
            'angles': [],
            'min_angles': [],
            'max_angles': []
        }
        
        for simplex in simplices:
            # Pobranie wierzchołków trójkąta
            vertices = points[simplex]
            
            # Jakość kształtu
            quality = self.calculate_triangle_quality(vertices)
            statistics['quality_values'].append(quality)
            
            # Pole
            area = self.calculate_triangle_area(vertices)
            statistics['areas'].append(area)
            
            # Kąty
            angles = self.calculate_angles(vertices)
            statistics['angles'].extend(angles)
            statistics['min_angles'].append(np.min(angles))
            statistics['max_angles'].append(np.max(angles))
        
        # Obliczanie statystyk zbiorczych
        statistics['quality_mean'] = np.mean(statistics['quality_values'])
        statistics['quality_median'] = np.median(statistics['quality_values'])
        statistics['quality_std'] = np.std(statistics['quality_values'])
        statistics['quality_min'] = np.min(statistics['quality_values'])
        statistics['quality_max'] = np.max(statistics['quality_values'])
        
        statistics['area_mean'] = np.mean(statistics['areas'])
        statistics['area_std'] = np.std(statistics['areas'])
        statistics['area_total'] = np.sum(statistics['areas'])
        
        statistics['angle_min'] = np.min(statistics['angles'])
        statistics['angle_max'] = np.max(statistics['angles'])
        statistics['angle_mean'] = np.mean(statistics['angles'])
        
        # Histogram jakości
        statistics['quality_histogram'], statistics['quality_bins'] = np.histogram(
            statistics['quality_values'], bins=20, range=(0, 1)
        )
        
        return statistics
    
    def print_statistics(self, stats):
        """Wyświetla statystyki w czytelnej formie"""
        print(f"Liczba trójkątów: {stats['num_triangles']}")
        print(f"Całkowite pole triangulacji: {stats['area_total']:.4f}")
        print("\nJakość kształtów:")
        print(f"  Średnia: {stats['quality_mean']:.4f}")
        print(f"  Mediana: {stats['quality_median']:.4f}")
        print(f"  Odchylenie standardowe: {stats['quality_std']:.4f}")
        print(f"  Minimum: {stats['quality_min']:.4f}")
        print(f"  Maksimum: {stats['quality_max']:.4f}")
        print("\nKąty:")
        print(f"  Najmniejszy kąt: {stats['angle_min']:.2f}°")
        print(f"  Największy kąt: {stats['angle_max']:.2f}°")
        print(f"  Średni kąt: {stats['angle_mean']:.2f}°")