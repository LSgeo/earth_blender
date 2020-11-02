#include "mex.h"

#include <igl/local_basis.h>
#include <igl/copyleft/comiso/nrosy.h>

#include <igl/matlab/prepare_lhs.h>
#include <igl/matlab/parse_rhs.h>

#include <igl/PI.h>

// Mesh
Eigen::MatrixXd V;
Eigen::MatrixXi F;

// Constrained faces id
Eigen::VectorXi b;

// Cosntrained faces representative vector
Eigen::MatrixXd bc;

// Degree of the N-RoSy field
int N = 6;

// Converts a representative vector per face in the full set of vectors that describe
// an N-RoSy field
void representative_to_nrosy(
  const Eigen::MatrixXd& V,
  const Eigen::MatrixXi& F,
  const Eigen::MatrixXd& R,
  const int N,
  Eigen::MatrixXd& Y)
{
  using namespace Eigen;
  using namespace std;
  MatrixXd B1, B2, B3;

  igl::local_basis(V,F,B1,B2,B3);

  Y.resize(F.rows()*N,3);
  for (unsigned i=0;i<F.rows();++i)
  {
    double x = R.row(i) * B1.row(i).transpose();
    double y = R.row(i) * B2.row(i).transpose();
    double angle = atan2(y,x);

    for (unsigned j=0; j<N;++j)
    {
      double anglej = angle + 2*igl::PI*double(j)/double(N);
      double xj = cos(anglej);
      double yj = sin(anglej);
      Y.row(i*N+j) = xj * B1.row(i) + yj * B2.row(i);
    }
  }
}

/* The gateway function */
void mexFunction( int nlhs, mxArray *plhs[],
                  int nrhs, const mxArray *prhs[])
{ 
    igl::matlab::parse_rhs_double(prhs,V);
    igl::matlab::parse_rhs_index(prhs+1,F);
    
    // Threshold faces with high anisotropy
    b.resize(1);
    b << 0;
    bc.resize(1,3);
    bc << 1,1,1;

    // Runs the nrosy
    MatrixXd R; //output field
    VectorXd S; //output singularities 

    igl::copyleft::comiso::nrosy(V,F,b,bc,VectorXi(),VectorXd(),MatrixXd(),N,0.5,R,S);
    
    Eigen::MatrixXd Y;
    representative_to_nrosy(V, F, R, N, Y);
    
    // Return the matrices to matlab
      switch(nlhs)
      {
        case 2:
          igl::matlab::prepare_lhs_double(S,plhs+1);
        case 1:
          igl::matlab::prepare_lhs_double(Y,plhs);
        default: break;
      }
}