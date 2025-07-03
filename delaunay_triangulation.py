import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import time
from bowyer_watson import BowyerWatsonTriangulation
from statistics_collector import TriangulationStatistics
from visualization import Visualizer

def generate_test_points(n_points=50, seed=None):
    if seed is not None:
        np.random.seed(seed)
    points = np.random.rand(n_points, 2) * 100
    return points

def run_triangulation_comparison(points):
    results = {}
    
    #implementacja Bowyer-Watson
    print("Wykonywanie triangulacji metodą Bowyer-Watson...")
    start_time = time.time()
    bw_triangulation = BowyerWatsonTriangulation()
    bw_triangles = bw_triangulation.triangulate(points)
    bw_time = time.time() - start_time
    
    # Konwersja do formatu indeksów
    bw_simplex_indices = []
    for triangle in bw_triangles:
        indices = []
        for vertex in triangle:
            idx = np.where((points == vertex).all(axis=1))[0]
            if len(idx) > 0:
                indices.append(idx[0])
        if len(indices) == 3:
            bw_simplex_indices.append(indices)
    
    results['bowyer_watson'] = {
        'triangles': bw_triangles,
        'simplices': np.array(bw_simplex_indices),
        'time': bw_time
    }
    
    #Implementacja scipy.Delaunay
    print("Wykonywanie triangulacji metodą scipy.Delaunay...")
    start_time = time.time()
    scipy_tri = Delaunay(points)
    scipy_time = time.time() - start_time
    
    results['scipy'] = {
        'triangulation': scipy_tri,
        'simplices': scipy_tri.simplices,
        'time': scipy_time
    }
    
    return results

def main():
    print("=== Triangulacja Delaunay'a - porównanie metod ===\n")
    
    # Generowanie punktów testowych
    points = generate_test_points(n_points=100, seed=42)
    print(f"Wygenerowano {len(points)} punktów testowych")
    
    # Wykonanie triangulacji obiema metodami
    results = run_triangulation_comparison(points)
    
    # Zbieranie statystyk
    stats_collector = TriangulationStatistics()
    
    print("\n=== Statystyki dla metody Bowyer-Watson ===")
    bw_stats = stats_collector.calculate_statistics(
        points, results['bowyer_watson']['simplices']
    )
    stats_collector.print_statistics(bw_stats)
    
    print("\n=== Statystyki dla metody scipy.Delaunay ===")
    scipy_stats = stats_collector.calculate_statistics(
        points, results['scipy']['simplices']
    )
    stats_collector.print_statistics(scipy_stats)
    
    print("\n=== Porównanie czasów wykonania ===")
    print(f"Bowyer-Watson: {results['bowyer_watson']['time']:.6f} s")
    print(f"scipy.Delaunay: {results['scipy']['time']:.6f} s")
    print(f"Różnica: {results['bowyer_watson']['time'] - results['scipy']['time']:.6f} s")
    
    # Wizualizacja
    visualizer = Visualizer()
    
    # Wykres porównawczy triangulacji
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    fig.suptitle('Porównanie triangulacji Delaunay\'a')
    
    visualizer.plot_triangulation(
        points, results['bowyer_watson']['simplices'], 
        ax1, "Bowyer-Watson (własna implementacja)"
    )
    
    visualizer.plot_triangulation(
        points, results['scipy']['simplices'], 
        ax2, "scipy.Delaunay"
    )
    
    plt.tight_layout()
    plt.show()
    
    # Histogram jakości kształtów
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Histogram jakości kształtów')
    
    visualizer.plot_quality_histogram(bw_stats['quality_values'], ax1, "Bowyer-Watson")
    visualizer.plot_quality_histogram(scipy_stats['quality_values'], ax2, "scipy.Delaunay")
    
    plt.tight_layout()
    plt.show()
    
    # Porównanie statystyk
    visualizer.plot_statistics_comparison({
        'Bowyer-Watson': bw_stats,
        'scipy.Delaunay': scipy_stats
    })

if __name__ == "__main__":
    main()