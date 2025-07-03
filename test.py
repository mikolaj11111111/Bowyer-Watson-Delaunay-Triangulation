
import numpy as np
import matplotlib.pyplot as plt
from delaunay_triangulation import main, generate_test_points, run_triangulation_comparison
from visualization import Visualizer
from statistics_collector import TriangulationStatistics

def test_random_points():
    """Test na większym zbiorze losowych punktów"""
    # Generowanie różnych konfiguracji punktów
    np.random.seed(42)
    
    # 1. Punkty losowe równomiernie rozłożone
    uniform_points = generate_test_points(100, seed=42)
    
    # 2. Punkty skupione w klastrach
    cluster_points = np.vstack([
        np.random.normal(25, 5, (25, 2)),
        np.random.normal(75, 5, (25, 2)),
        np.random.normal([25, 75], 5, (25, 2)),
        np.random.normal([75, 25], 5, (25, 2))
    ])
    
    # 3. Punkty na okręgu
    angles = np.linspace(0, 2*np.pi, 50, endpoint=False)
    circle_points = np.column_stack([
        50 + 30 * np.cos(angles),
        50 + 30 * np.sin(angles)
    ])
    # Dodajemy punkty w środku
    circle_points = np.vstack([circle_points, [[50, 50]]])
    
    # Testowanie każdej konfiguracji
    configurations = {
        'Uniform': uniform_points,
        'Clusters': cluster_points,
        'Circle': circle_points
    }
    
    for name, points in configurations.items():
        print(f"\n=== Test konfiguracji: {name} ===")
        results = run_triangulation_comparison(points)
        
        # Statystyki
        stats_collector = TriangulationStatistics()
        bw_stats = stats_collector.calculate_statistics(
            points, results['bowyer_watson']['simplices']
        )
        scipy_stats = stats_collector.calculate_statistics(
            points, results['scipy']['simplices']
        )
        
        # Wizualizacja z jakością kształtów
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))
        fig.suptitle(f'Triangulacja - {name}')
        
        visualizer = Visualizer()
        
        # Zwykła triangulacja
        visualizer.plot_triangulation(
            points, results['bowyer_watson']['simplices'], 
            ax1, "Bowyer-Watson"
        )
        visualizer.plot_triangulation(
            points, results['scipy']['simplices'], 
            ax2, "scipy.Delaunay"
        )
        
        # Triangulacja kolorowana jakością
        visualizer.plot_triangulation_colored_by_quality(
            points, results['bowyer_watson']['simplices'],
            bw_stats['quality_values'], ax3, "Bowyer-Watson (jakość)"
        )
        visualizer.plot_triangulation_colored_by_quality(
            points, results['scipy']['simplices'],
            scipy_stats['quality_values'], ax4, "scipy.Delaunay (jakość)"
        )
        
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    print("=== Testy triangulacji Delaunay'a ===\n")
        
    # 2. Test różnych konfiguracji punktów
    print("\n2. Test różnych konfiguracji punktów...")
    test_random_points()
    
    main()