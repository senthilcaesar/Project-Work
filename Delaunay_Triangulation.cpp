#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Triangulation_3.h>
#include <CGAL/Delaunay_triangulation_3.h>
#include <CGAL/Triangulation_ds_vertex_base_3.h>
#include <CGAL/IO/write_off_points.h>
#include <CGAL/poisson_surface_reconstruction.h>
#include <CGAL/Triangulation_data_structure_3.h>
#include <CGAL/Triangulation_vertex_base_3.h>
#include <CGAL/Triangulation_vertex_base_with_info_3.h>
#include <CGAL/Triangulation_cell_base_3.h>
#include <CGAL/convex_hull_3.h>
#include <boost/iterator/zip_iterator.hpp>
#include <iostream>
#include <vector>
#include <fstream>
#include <iostream>
using namespace std;

// Main Kernel Class
typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
// Instantiating with Kernel Inorder to access the Objects and Predicate functions of the kernel
typedef CGAL::Triangulation_vertex_base_3<K>				vbl;
typedef CGAL::Triangulation_cell_base_3<K>				cb;
// Custom class to add Global Index to each vertices
typedef CGAL::Triangulation_vertex_base_with_info_3<unsigned, K>	vb;
// This DS class requires 2 parameters to be passed which are VERTEX class and CELL class
typedef CGAL::Triangulation_data_structure_3<vb, cb>		        Tds;
// This Triangulation class generally requires 2 parameters, one trait class and another Data structure class
typedef CGAL::Delaunay_triangulation_3<K, Tds>				DTriangle_3;
typedef DTriangle_3::Point						Point_3;
typedef CGAL::Polyhedron_3<K>						Polyhedron;

// K Simplex Iterators
DTriangle_3::Finite_cells_iterator					cit;
DTriangle_3::Finite_vertices_iterator				        vit;
DTriangle_3::Finite_edges_iterator					eit;
DTriangle_3::Finite_facets_iterator					fit;

// Handles
DTriangle_3::Cell_handle						ch;
DTriangle_3::Vertex_handle						vh;

int main() {

	std::ifstream is("2omz.xyz");
	std::istream_iterator<Point_3> start(is), end;
	std::vector<Point_3> V(start, end);
	vector<unsigned> indices;
	for(int i = 0; i < V.size(); i++) { indices.push_back(i); }

	// Ddelaunay Triangulation
	DTriangle_3 t( boost::make_zip_iterator(boost::make_tuple(V.begin(),indices.begin())),
              boost::make_zip_iterator(boost::make_tuple(V.end(),indices.end())));
	
	cout << "The number of Finite Edges = ";
	cout << t.number_of_finite_edges() << endl;
	cout << "The number of Finite Faces = ";
	cout << t.number_of_finite_facets() << endl;
	cout << "The number of Finite Cells = ";
	cout << t.number_of_finite_cells() << endl;
	cout << "The number of Finite Vertices = ";
	cout << t.number_of_vertices() << endl;

for (fit = t.finite_facets_begin(); fit != t.finite_facets_end(); fit++) {

		cout << fit->first->vertex((fit->second+1)%4)->point() << " --- ";
		cout << fit->first->vertex((fit->second+1)%4)->info();
		cout << fit->first->vertex((fit->second+2)%4)->point() << " --- ";
		cout << fit->first->vertex((fit->second+2)%4)->info();
		cout << fit->first->vertex((fit->second+3)%4)->point() << " --- ";
		cout << fit->first->vertex((fit->second+3)%4)->info() << endl;
	}

  // Find Neighbour Cell vertices
  int i = 0;
  for(cit = t.finite_cells_begin(); cit != t.finite_cells_end(); cit++) {
	  ch = cit;
	  cout << ch->neighbor(i)->vertex(1)->point() << endl;
	  i++;
	}

  for(cit = t.finite_cells_begin(); cit != t.finite_cells_end(); ++cit) {

	  cout << "V[0] = " << cit->vertex(0)->point() << endl;
	  cout << "V[1] = " << cit->vertex(1)->point() << endl;
	  cout << "V[2] = " << cit->vertex(2)->point() << endl;
	  cout << "V[3] = " << cit->vertex(3)->point() << endl;

  }

 // Write to OFF file format
  std::ofstream out("project_2omz.off");
  CGAL::set_ascii_mode( std::cout);

  out << "OFF" << std::endl << t.number_of_vertices() << ' '
              << t.number_of_finite_facets() << " 0" << std::endl;
  std::copy( V.begin(), V.end(),
               std::ostream_iterator<Point_3>(out, "\n"));
 for (fit = t.finite_facets_begin(); fit != t.finite_facets_end(); fit++) {
	out << "3 ";
	out << fit->first->vertex((fit->second+1)%4)->info() << " ";
	out << fit->first->vertex((fit->second+2)%4)->info() << " ";
	out << fit->first->vertex((fit->second+3)%4)->info() << endl;
	}
}
