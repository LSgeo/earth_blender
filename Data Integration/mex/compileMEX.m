clear all
mex -n harm_mex.cpp -I../../../libigl_dev/libigl/include -I../../../libigl_dev/libigl/external/eigen
mex -v lscm_mex.cpp -I../libigl/include -I../libigl/external/eigen

mex -v readPLY_mex.cpp -I../../libigl_dev/libigl/include -I../../libigl_dev/libigl/external/eigen
mex -v readOFF_mex.cpp -I../../libigl_dev/libigl/include -I../../libigl_dev/libigl/external/eigen

mex -v nrosy_mex.cpp -I../../../libigl_dev/libigl/include -I../../../libigl_dev/libigl/external/eigen -I../../../libigl_dev/libigl/include/igl/copyleft/comiso
%-I../../libigl_dev/libigl/external/CoMISo/Solver -I../../libigl_dev/libigl/external/CoMISo/ext/gmm-4.2/include -I../../libigl_dev/libigl/external/CoMISo/ext/OpenBLAS-v0.2.14-Win64-int64/include

[V,F] = readOBJ_mex('./new_v84_remesh.obj');

V_uv = lscm_mex(V,F);

%% Plot the mesh
%trimesh(F,V(:,1),V(:,2),V(:,3));
trimesh(F,V_uv(:,1),V_uv(:,2));
axis vis3d;



% C:\ProgramData\MATLAB\SupportPackages\R2018b\3P.instrset\mingw_w64.instrset\bin\g++ -c -DMATLAB_DEFAULT_RELEASE=R2017b  -DUSE_MEX_CMD   -m64 -DMATLAB_MEX_FILE  -I"..\..\libigl_dev\libigl\include" -I"..\..\libigl_dev\libigl\external\eigen"  -I"C:\Program Files\MATLAB\R2018b/extern/include" -I"C:\Program Files\MATLAB\R2018b/simulink/include" -fexceptions -fno-omit-frame-pointer -std=c++11 -O2 -fwrapv -DNDEBUG "D:\repos\geometry_processing\mex\nrosy_mex.cpp" -o C:\Users\David\AppData\Local\Temp\mex_36574857362708_3780\nrosy_mex.obj
% C:\ProgramData\MATLAB\SupportPackages\R2018b\3P.instrset\mingw_w64.instrset\bin\g++ -c -DMATLAB_DEFAULT_RELEASE=R2017b  -DUSE_MEX_CMD   -m64 -DMATLAB_MEX_FILE  -I"..\..\libigl_dev\libigl\include" -I"..\..\libigl_dev\libigl\external\eigen"  -I"C:\Program Files\MATLAB\R2018b/extern/include" -I"C:\Program Files\MATLAB\R2018b/simulink/include" -fexceptions -fno-omit-frame-pointer -std=c++11 -O2 -fwrapv -DNDEBUG "C:\Program Files\MATLAB\R2018b\extern\version\cpp_mexapi_version.cpp" -o C:\Users\David\AppData\Local\Temp\mex_36574857362708_3780\cpp_mexapi_version.obj
% C:\ProgramData\MATLAB\SupportPackages\R2018b\3P.instrset\mingw_w64.instrset\bin\g++ -m64 -Wl,--no-undefined -shared -static -s -Wl,"C:\Program Files\MATLAB\R2018b/extern/lib/win64/mingw64/exportsmexfileversion.def" C:\Users\David\AppData\Local\Temp\mex_36574857362708_3780\nrosy_mex.obj C:\Users\David\AppData\Local\Temp\mex_36574857362708_3780\cpp_mexapi_version.obj   -L"C:\Program Files\MATLAB\R2018b\extern\lib\win64\mingw64" -llibmx -llibmex -llibmat -lm -llibmwlapack -llibmwblas -llibMatlabDataArray -llibMatlabEngine -o nrosy_mex.mexw64

g++ -c -DMATLAB_DEFAULT_RELEASE=R2017b  -DUSE_MEX_CMD   -m64 -DMATLAB_MEX_FILE  -I"..\..\libigl_dev\libigl\include" -I"..\..\libigl_dev\libigl\external\eigen"  -I"C:\Program Files\MATLAB\R2018b/extern/include" -I"C:\Program Files\MATLAB\R2018b/simulink/include" -fexceptions -fno-omit-frame-pointer -std=c++11 -O2 -fwrapv -DNDEBUG "D:\repos\geometry_processing\mex\nrosy_mex.cpp" -o C:\Users\David\AppData\Local\Temp\mex_36574857362708_3780\nrosy_mex.obj

C:\ProgramData\MATLAB\SupportPackages\R2018b\3P.instrset\mingw_w64.instrset\bin\g++ -c -DMATLAB_DEFAULT_RELEASE=R2017b  -DUSE_MEX_CMD   -m64 -DMATLAB_MEX_FILE  -I"..\..\..\libigl_dev\libigl\include" -I"..\..\..\libigl_dev\libigl\external\eigen"  -I"C:\Program Files\MATLAB\R2018b/extern/include" -I"C:\Program Files\MATLAB\R2018b/simulink/include" -fexceptions -fno-omit-frame-pointer -std=c++11 -O2 -fwrapv -DNDEBUG "D:\repos\geometry_processing\mex\nrosy\nrosy_mex.cpp" -o D:\repos\geometry_processing\mex\nrosy\nrosy_mex.obj
g++ -c -DMATLAB_DEFAULT_RELEASE=R2017b  -DUSE_MEX_CMD   -m64 -DMATLAB_MEX_FILE  -I"..\..\..\libigl_dev\libigl\include" -I"..\..\..\libigl_dev\libigl\external\eigen"  -I"C:\Program Files\MATLAB\R2018b/extern/include" -I"C:\Program Files\MATLAB\R2018b/simulink/include" -fexceptions -fno-omit-frame-pointer -std=c++11 -O2 -fwrapv -DNDEBUG "C:\Program Files\MATLAB\R2018b\extern\version\cpp_mexapi_version.cpp" -o D:\repos\geometry_processing\mex\nrosy\cpp_mexapi_version.obj
g++ -m64 -Wl,--no-undefined -shared -static -s -Wl,"C:\Program Files\MATLAB\R2018b/extern/lib/win64/mingw64/exportsmexfileversion.def" D:\repos\geometry_processing\mex\nrosy\nrosy_mex.obj D:\repos\geometry_processing\mex\nrosy\cpp_mexapi_version.obj   -L"C:\Program Files\MATLAB\R2018b\extern\lib\win64\mingw64" -llibmx -llibmex -llibmat -lm -llibmwlapack -llibmwblas -llibMatlabDataArray -llibMatlabEngine -o nrosy_mex.mexw64
