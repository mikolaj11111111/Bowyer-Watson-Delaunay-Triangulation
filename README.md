# Bowyer-Watson Delaunay Triangulation

## Description
Custom implementation of the Bowyer-Watson algorithm for Delaunay triangulation. Creates triangulations where no point lies inside the circumcircle of any triangle.

## Features
- **Incremental Construction** - Adds points one by one to build triangulation
- **Circumcircle Calculations** - Accurate geometric predicates
- **Super-triangle Method** - Handles boundary conditions elegantly
- **Numerical Stability** - Robust handling of edge cases

## Algorithm Steps
1. Create super-triangle encompassing all points
2. Add points incrementally
3. Remove triangles with violated circumcircle property
4. Retriangulate resulting polygon
5. Clean up super-triangle connections

## Usage
```python
triangulation = BowyerWatsonTriangulation()
triangles = triangulation.triangulate(points)
```
