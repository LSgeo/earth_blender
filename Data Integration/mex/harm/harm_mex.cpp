#include "mex.h"

#include <igl/boundary_loop.h>
#include <igl/harmonic.h>
#include <igl/map_vertices_to_circle.h>

#include <igl/matlab/prepare_lhs.h>
#include <igl/matlab/parse_rhs.h>
#include <Eigen/Core>

/* The gateway function */
void mexFunction( int nlhs, mxArray *plhs[],
                  int nrhs, const mxArray *prhs[])
{
    Eigen::MatrixXd V;
    Eigen::MatrixXi F;
    Eigen::MatrixXd V_uv;

    igl::matlab::parse_rhs_double(prhs,V);
    igl::matlab::parse_rhs_index(prhs+1,F);

    // Find the open boundary
    Eigen::VectorXi bnd;
    igl::boundary_loop(F,bnd);

    // Map the boundary to a circle, preserving edge proportions
    Eigen::MatrixXd bnd_uv;
    igl::map_vertices_to_circle(V,bnd,bnd_uv);

    // Harmonic parametrization for the internal vertices
    igl::harmonic(V,F,bnd,bnd_uv,1,V_uv);

    igl::matlab::prepare_lhs_index(V_uv,plhs);
}