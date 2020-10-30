clear all

mex -v readPLY_mex.cpp -I../../../libigl_dev_test/libigl/include -I../../../libigl_dev_test/libigl/external/eigen

[V,F]  = readPLY_mex('../lith2_remesh_test_v86.ply');
% 
% V_uv = lscm_mex(V,F);
% 
% %% Plot the mesh
trimesh(F,V(:,1),V(:,2),V(:,3));
% trimesh(F,V_uv(:,1),V_uv(:,2));
axis vis3d;

