# Delaunay Triangulation - Implementation and Comparison

A comprehensive implementation of the Delaunay triangulation algorithm using the Bowyer-Watson method, with comparison to scipy's implementation and detailed statistical analysis.

## Description

This project implements the Delaunay triangulation algorithm from scratch using the Bowyer-Watson method and compares it with scipy's built-in implementation. Delaunay triangulation is a method of dividing a plane into triangles such that no point lies inside the circumcircle of any triangle.

The project provides tools for:
- Custom implementation of the Bowyer-Watson algorithm
- Performance comparison with scipy.spatial.Delaunay
- Statistical analysis of triangulation quality
- Comprehensive visualization of results

## Features

### 🔧 **Algorithm Implementation**
- Complete Bowyer-Watson algorithm with super-triangle handling
- Circumcircle calculation for triangles
- Bad triangle detection and removal
- Polygon boundary reconstruction

### 📊 **Statistical Analysis**
- **Shape Quality Metrics** - ratio of inscribed to circumscribed circle radii
- **Angle Distribution** - analysis of minimum and maximum angles
- **Area Calculations** - total and average triangle areas
- **Quality Histograms** - distribution of shape quality metrics

### 🎨 **Visualization Tools**
- Triangulation plotting with points and edges
- Color-coded triangles by shape quality
- Statistical histograms and comparisons
- Side-by-side method comparisons

### 🧪 **Test Configurations**
- Uniformly distributed random points
- Clustered point configurations
- Points distributed on circles
- Performance benchmarking
