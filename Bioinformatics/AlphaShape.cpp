#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Delaunay_triangulation_3.h>
#include <CGAL/Alpha_shape_3.h>
#include <fstream>
#include <list>
#include <vector>
#include <cassert>
typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Alpha_shape_vertex_base_3<K>                  Vb;
typedef CGAL::Alpha_shape_cell_base_3<K>                    Fb;
typedef CGAL::Triangulation_data_structure_3<Vb,Fb>         Tds;
typedef CGAL::Delaunay_triangulation_3<K,Tds,CGAL::Fast_location>  Delaunay;
typedef CGAL::Alpha_shape_3<Delaunay>                       Alpha_shape_3;
typedef K::Point_3					    Point;
typedef Alpha_shape_3::Alpha_iterator			    Alpha_iterator;
typedef Alpha_shape_3::NT				    NT;
using namespace std;

typedef K::Point_3					    Point;
typedef Alpha_shape_3::Alpha_iterator			    Alpha_iterator;
typedef Alpha_shape_3::Cell_handle			    Cell_handle;
typedef Alpha_shape_3::Vertex_handle			    Vertex_handle;
typedef Alpha_shape_3::Facet				    Facet;
typedef Alpha_shape_3::Edge				    Edge;
typedef std::pair<Point, int>				    PointWithIndex;

int match_index(Point match, list<Vertex_handle> V) {
	int i = 0;
	for(std::list<Vertex_handle>::iterator vit = V.begin(); vit != V.end(); vit++) {

				Vertex_handle check = *vit;
				Point some = check->point();
				if ( match == some ) return i;
					i++;
	}
}

int main() {

    std::ifstream is("2omz.xyz");
    std::istream_iterator<Point> start(is), end;
    std::vector<Point> V(start, end);
    Delaunay dt(V.begin(), V.end());
  
  
  std::cout << "Delaunay computed." << std::endl;
  Alpha_shape_3 as(dt, 0, Alpha_shape_3::GENERAL);
  std::cout << "Alpha shape computed in REGULARIZED mode by defaut."
        << std::endl;

  // find optimal alpha value
	Alpha_shape_3::NT alpha_solid = as.find_alpha_solid();
	Alpha_iterator opt = as.find_optimal_alpha(1);
	std::cout << "Smallest alpha value to get a solid through data points is " << alpha_solid << std::endl;
	std::cout << "Optimal alpha value to get one connected component is " << *opt << std::endl;

		std::cout << "Using alpha value: " << alpha_solid << std::endl;

		as.set_alpha(*opt);

 /*int nrows = dt.number_of_vertices();*/
 /* std::vector<PointWithIndex> x(nrows);
  for (int i = 0; i < nrows; ++i) {
    x[i] = std::make_pair(
			  some_function_to_read_a_point(i),
			  i+1 // because this will be a row index in Matlab, 1, ..., Nrows
			  );
  }*/

	std::list<Vertex_handle>	vertices;
	std::list<Cell_handle>		cells;
	std::list<Facet>		facets;
	std::list<Edge>			edges;


	as.get_alpha_shape_vertices(std::back_inserter(vertices), Alpha_shape_3::REGULAR);
	as.get_alpha_shape_cells(std::back_inserter(cells), Alpha_shape_3::INTERIOR);
	as.get_alpha_shape_facets(std::back_inserter(facets), Alpha_shape_3::REGULAR);
	as.get_alpha_shape_facets(std::back_inserter(facets), Alpha_shape_3::SINGULAR);
	as.get_alpha_shape_edges(std::back_inserter(edges), Alpha_shape_3::REGULAR);
  
	std::cout << as.number_of_vertices() << std::endl;
	std::cout << "Number of alphas: " << as.number_of_alphas()  << std::endl;
	std::cout << vertices.size()  << " vertices" << std::endl;
	std::cout << cells.size() << " interior tetrahedra" << std::endl;
	std::cout << facets.size() << " boundary facets" << std::endl;
	std::cout << edges.size()  << " boundary edges" << std::endl;


	  std::ofstream out("C:/Users/toshiba/Desktop/612 - Nurit/Project/sample inputs/2omz_alpha.off");
	CGAL::set_ascii_mode( std::cout);
	
	out << "OFF" << std::endl << vertices.size() << ' '
              << facets.size() << " 0" << std::endl;
	/*std::copy( vertices.begin(), vertices.end(),
               std::ostream_iterator<Point>(out, "\n"));*/
	for(std::list<Vertex_handle>::iterator vit = vertices.begin(); vit != vertices.end(); ++vit) {

				Vertex_handle some = *vit;
				out << some->point() << endl;
	}
	
	for (std::list<Facet>::iterator it = facets.begin(); it != facets.end(); ++it) { 
		out << "3 ";
		Point Match1 = it->first->vertex((it->second+1)%4)->point();
		out << match_index(Match1, vertices) << " ";
		Point Match2 = it->first->vertex((it->second+2)%4)->point();
		out << match_index(Match2, vertices) << " ";
		Point Match3 = it->first->vertex((it->second+3)%4)->point();
		out << match_index(Match3, vertices) << endl;

  }

}
