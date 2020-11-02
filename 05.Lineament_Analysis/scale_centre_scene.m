clear all

addpath('./mex/');
addpath('./mex/readPLY/');
addpath('./mex/readOFF/');

proj_dir = 'iocg_fluid';
in_dir   = '/obj/';
out_dir  = '/obj_xz-y/';

objects = dir(['./' proj_dir in_dir]); 
objects = objects(~cellfun('isempty', {objects.date}));
t = struct2table(objects);
t(1:2,:) = [];
fnames = t.name;

objects_struct = struct;

cd(['./' proj_dir]);
rmdir(['.' out_dir], 's');
mkdir(['.' out_dir]);

% rasterfname = 'georaster.tif';
% [A,R] = readgeoraster(rasterfname);
%info = georasterinfo(rasterfname);

%read in clipping region
% S =shaperead('./clipping_region.shp');
% xlimits = S.BoundingBox(1,:);
% ylimits = S.BoundingBox(2,:);
% rasterSize = R.RasterSize;
% 
% R_proj = maprefcells(xlimits,ylimits,rasterSize, ...
%     'ColumnsStartFrom',R.ColumnsStartFrom);

for f=1:size(fnames,1)

    in_fname = ['.' in_dir fnames{f}];
    [V,F] = readOBJ_mex(in_fname);
    %flip y-direction
    V(:,2) = -V(:,2);
    % swap y and z dimenions
    V = [V(:,1) V(:,3) V(:,2)];
    objects_struct(f).name = fnames{f};
    objects_struct(f).V = V(:,1:3);
    objects_struct(f).F = F;
    
    vmin = min(V);
    vmax = max(V);
    centre = mean(V);
    
    objects_struct(f).vmin = vmin;
    objects_struct(f).vmax = vmax;
    objects_struct(f).centre = centre;       
end

t2 = struct2table(objects_struct);
q =t2.V;
q = cell2mat(q);
extent = reshape([min(q);max(q)],1,6);

centre = mean(reshape(extent,2,3));
%ext = range(reshape(extent,2,3));
ext = max(q) - min(q);
asp_ratio = ext./norm(ext);
% centre each object
for c=1:size(objects_struct,2)
    V2 = (objects_struct(c).V - ...
                repmat(min(q), size(objects_struct(c).V,1),1))...
                ./repmat(ext, size(objects_struct(c).V,1),1);
    V2 = V2.*repmat(asp_ratio, size(objects_struct(c).V,1),1);                    
    %V2(:,2) = objects_struct(c).V(:,2);        
    objects_struct(c).V2 = V2;        
    out_fname = ['.' out_dir objects_struct(c).name];
    writeOBJ(out_fname,objects_struct(c).V,objects_struct(c).F);
end

% rout_fname = ['.' out_dir rasterfname '_cn' '.tif'];
% R_cn = maprefcells([0 asp_ratio(1)],[0 asp_ratio(3)],rasterSize, ...
%     'ColumnsStartFrom',R.ColumnsStartFrom);
% geotiffwrite(rout_fname, A, R_cn);