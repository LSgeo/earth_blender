clear all

%% Best Params
% scale_offset=1.2;
% scale_step =10;
% bin_sizes =[60,60];
% contourgrid_res_x = 800;
% contourgrid_res_y = 800;
% c_lvls = 0:0.1425:1.0;

addpath('./pktools/');
L_all = shaperead('./shp/lineaments_clipped.shp');
%L = shaperead('./shp/gravity_worms_clipped.shp');   


all_z = [L_all(:).z_mean];

heights_all = unique([L_all(:).z_mean]);
h_sort_all=sort(heights_all,'descend');
mid_point = floor(size(h_sort_all,2)/2);

upper_hsort = 1:mid_point;
lower_hsort = mid_point+1:size(h_sort_all,2);

h_sort=lower_hsort;
heights = h_sort_all(h_sort);

L = L_all(find(all_z>h_sort_all(mid_point)));
all_depths = [L(:).z_mean];

scale_offset=1.2;
scale_step =10;
bin_sizes =[60,60];
contourgrid_res_x = 800;
contourgrid_res_y = 800;
c_lvls = 0:0.1425:1.0;

ratio_filts = h_sort./h_sort(end);
sigmas = scale_step.*ratio_filts+scale_offset;

%% bin centers
bc = struct;
% array of bins of lineaments in XY for each height
N = [];
% array of gaussian blur of density of lineaments, standard deviation 
% scaled by depth values
G=[];

O = zeros(bin_sizes);

for idz=1:size(heights,2)
    XY_data =  [[L(find(all_depths==heights(idz))).X]',[L(find(all_depths==heights(idz))).Y]'];
    [H,c] = hist3([],'Nbins',bin_sizes);
    N = cat(3,N,H);
    bc(idz).bin_centers = c;
    I = imgaussfilt(H,sigmas(idz));
    G = cat(3,G,I);
    O = O+I;
end

% reorient the summed lineament density georeferencing
O = rot90(fliplr(O));

% arrays of of bin centers from all depths
all_grid_x = [];
all_grid_y = [];
%figure;
for i=1:size(heights,2)
    c = bc(i).bin_centers;
    xh = c{1};yh=c{2};
    [X,Y] = ndgrid(xh,yh);
    %plot(X(:),Y(:),'o');hold all
    all_grid_x = cat(3,all_grid_x,X);
    all_grid_y = cat(3,all_grid_y,Y);
end

% take average xy across all depths are gridding cell centers
grid_avg_x = sum(all_grid_x,3)./size(heights,2);
grid_avg_y = sum(all_grid_y,3)./size(heights,2);

%plot(grid_avg_x(:),grid_avg_y(:),'+');

% the gridding cell centers
x = mean(grid_avg_x');y=mean(grid_avg_y)';
%figure;imagesc(x,y,rot90(fliplr(O)));ax=gca;ax.YDir='normal';

% raster information cells
cellsize_x  = mean(diff(x));
cellsize_y = mean(diff(y));
rasterSize = size(O);
y_wlimits = [min(y)-0.5.*cellsize_y max(y)+0.5.*cellsize_y];
x_wlimits = [min(x)-0.5.*cellsize_x max(x)+0.5.*cellsize_x];

R = maprasterref('RasterSize', rasterSize, ...
          'YWorldLimits', y_wlimits, 'ColumnsStartFrom','south', ...
          'XWorldLimits', x_wlimits);

% O2 = rot90(fliplr(O));
% figure;mapshow(O,R);
%figure;imagesc(O);ax=gca;ax.YDir='normal';colorbar

% H1 = N(:,:,10);
% L1 = L(find(all_z==h_sort(10)));
% figure;
% mapshow(L1);

figure;
mapshow(applycolourmap(O,cmap('R1')),R);
% 
% 
% figure;imagesc(G(:,:,10));
% figure;imagesc(H1);

% figure;
% imagesc(c{1},c{2},flipud(G(:,:,1)));
% set(gca,'YDir','normal')
% colorbar;

% thresh = multithresh(O,5);
% seg_I = imquantize(O,thresh);
% RGB = label2rgb(seg_I); 	 
% figure;
% imshow(RGB);
% axis off

% [bcx,bcy] = meshgrid(c{1},c{2});
% figure;
% contourf(bcx,bcy,O,30);

% high res raster for contouring
[X,Y] = ndgrid(x,y);
F = griddedInterpolant(X,Y,O,'spline');
[Xq,Yq] = ndgrid(linspace(min(x),max(x),contourgrid_res_x),linspace(min(y),max(y),contourgrid_res_y));

% raster information cells for highres  raster
% the gridding cell centers
x_hr = mean(Xq');y_hr=mean(Yq)';

cellsizehr_x  = mean(diff(x_hr));
cellsizehr_y = mean(diff(y_hr));
rasterSize_hr = [contourgrid_res_x contourgrid_res_y];
yhr_wlimits = [min(y_hr)-0.5.*cellsizehr_y max(y_hr)+0.5.*cellsizehr_y];
xhr_wlimits = [min(x_hr)-0.5.*cellsizehr_x max(x_hr)+0.5.*cellsizehr_x];

R_hr = maprasterref('RasterSize', rasterSize_hr, ...
          'YWorldLimits', yhr_wlimits, 'ColumnsStartFrom','south', ...
          'XWorldLimits', xhr_wlimits);

Oq = F(Xq,Yq);

figure;
mapshow(applycolourmap(Oq,cmap('R1')),R_hr);


figure;
contourf(Xq,Yq,Oq,c_lvls);
%contourf(Xq,Yq,Oq,15);
colorbar


% coordRefSysCode = 28353;
% filename = './lineaments_density_stacking.tif';
% geotiffwrite(filename, Oq, R_hr, 'CoordRefSysCode', coordRefSysCode);








