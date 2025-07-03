"""
Moduł do wizualizacji triangulacji i statystyk
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

class Visualizer:
    """Klasa do wizualizacji triangulacji"""
    
    def plot_triangulation(self, points, simplices, ax=None, title="Triangulacja Delaunay'a"):
        """Rysuje triangulację"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        
        # Rysowanie trójkątów
        for simplex in simplices:
            triangle = points[simplex]
            poly = Polygon(triangle, fill=False, edgecolor='b', linewidth=1)
            ax.add_patch(poly)
        
        # Rysowanie punktów
        ax.scatter(points[:, 0], points[:, 1], c='r', s=30, zorder=5)
        
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, alpha=0.3)
        
        return ax
    
    def plot_quality_histogram(self, quality_values, ax=None, title="Histogram jakości kształtów"):
        """Rysuje histogram jakości kształtów"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        ax.hist(quality_values, bins=20, range=(0, 1), alpha=0.7, edgecolor='black')
        ax.set_xlabel('Jakość kształtu')
        ax.set_ylabel('Liczba trójkątów')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        # Dodanie linii średniej i mediany
        mean_quality = np.mean(quality_values)
        median_quality = np.median(quality_values)
        
        ax.axvline(mean_quality, color='r', linestyle='--', linewidth=2, 
                   label=f'Średnia: {mean_quality:.3f}')
        ax.axvline(median_quality, color='g', linestyle='--', linewidth=2, 
                   label=f'Mediana: {median_quality:.3f}')
        
        ax.legend()
        
        return ax
    
    def plot_angle_distribution(self, angles, ax=None, title="Rozkład kątów"):
        """Rysuje rozkład kątów w trójkątach"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        ax.hist(angles, bins=30, range=(0, 180), alpha=0.7, edgecolor='black')
        ax.set_xlabel('Kąt [°]')
        ax.set_ylabel('Liczba wystąpień')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        # Idealny kąt dla trójkąta równobocznego
        ax.axvline(60, color='r', linestyle='--', linewidth=2, 
                   label='Kąt idealny (60°)')
        
        ax.legend()
        
        return ax
    
    def plot_statistics_comparison(self, stats_dict):
        """Porównuje statystyki różnych metod"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Porównanie statystyk triangulacji')
        
        methods = list(stats_dict.keys())
        colors = ['blue', 'orange', 'green', 'red'][:len(methods)]
        
        # 1. Porównanie jakości średniej
        ax = axes[0, 0]
        qualities = [stats_dict[method]['quality_mean'] for method in methods]
        bars = ax.bar(methods, qualities, color=colors)
        ax.set_ylabel('Średnia jakość kształtów')
        ax.set_title('Średnia jakość kształtów')
        ax.set_ylim(0, 1)
        
        # Dodanie wartości na słupkach
        for bar, quality in zip(bars, qualities):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{quality:.3f}', ha='center', va='bottom')
        
        # 2. Porównanie odchylenia standardowego jakości
        ax = axes[0, 1]
        stds = [stats_dict[method]['quality_std'] for method in methods]
        bars = ax.bar(methods, stds, color=colors)
        ax.set_ylabel('Odchylenie standardowe jakości')
        ax.set_title('Odchylenie standardowe jakości')
        
        # 3. Porównanie minimalnych kątów
        ax = axes[1, 0]
        min_angles = [stats_dict[method]['angle_min'] for method in methods]
        bars = ax.bar(methods, min_angles, color=colors)
        ax.set_ylabel('Minimalny kąt [°]')
        ax.set_title('Najmniejszy kąt w triangulacji')
        
        # 4. Porównanie maksymalnych kątów
        ax = axes[1, 1]
        max_angles = [stats_dict[method]['angle_max'] for method in methods]
        bars = ax.bar(methods, max_angles, color=colors)
        ax.set_ylabel('Maksymalny kąt [°]')
        ax.set_title('Największy kąt w triangulacji')
        
        plt.tight_layout()
        plt.show()
    
    def plot_triangulation_colored_by_quality(self, points, simplices, quality_values, 
                                            ax=None, title="Triangulacja z jakością kształtów"):
        """Rysuje triangulację z kolorami odpowiadającymi jakości kształtów"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        
        # Normalizacja kolorów
        from matplotlib.colors import Normalize
        from matplotlib.cm import ScalarMappable
        
        norm = Normalize(vmin=0, vmax=1)
        sm = ScalarMappable(norm=norm, cmap='viridis')
        
        # Rysowanie trójkątów z kolorami
        for simplex, quality in zip(simplices, quality_values):
            triangle = points[simplex]
            color = sm.to_rgba(quality)
            poly = Polygon(triangle, facecolor=color, edgecolor='black', 
                          linewidth=0.5, alpha=0.8)
            ax.add_patch(poly)
        
        # Rysowanie punktów
        ax.scatter(points[:, 0], points[:, 1], c='red', s=20, zorder=5)
        
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        # Kolorowa skala
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label('Jakość kształtu')
        
        return ax