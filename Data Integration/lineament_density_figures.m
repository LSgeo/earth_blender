clear all

addpath('./pktools/');

%L = shaperead('./shp/lineaments_clipped.shp');
L = shaperead('./shp/gravity_worms_clipped.shp');   

heights = unique([L(:).z_mean]);
h_sort=sort(heights,'descend');
all_z = [L(:).z_mean];

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
    [H,c] = hist3([[L(find(all_z==h_sort(idz))).X]',[L(find(all_z==h_sort(idz))).Y]'],'Nbins',bin_sizes);
    N = cat(3,N,H);
    bc(idz).bin_centers = c;
    I = imgaussfilt(H,sigmas(idz));
    G = cat(3,G,I);
    O = O+I;
end 




% reorient the summed lineament density georeferencing
% O = rot90(fliplr(O));
% figure;imagesc(O);ax=gca;ax.YDir='normal';



ind_hsort = 4;

H1 = rot90(fliplr(N(:,:,ind_hsort)));
L1 = L(find(all_z==h_sort(ind_hsort)));
G1 = rot90(fliplr(G(:,:,ind_hsort)));

R = create_georasterref(bc(ind_hsort).bin_centers{1},bc(ind_hsort).bin_centers{2},size(O));

figure;
ax2 = subplot(3,3,2);
mapshow(applycolourmap(H1,cmap('R1')),R);
title('Lineament Histogram');
set(ax2,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax2.XAxis.Exponent = 0;
xtickformat(ax2,'%.0f');

ax2.YAxis.Exponent = 0;
ytickformat(ax2,'%.0f');

% xlim(ax2,ax1.XLim);
% ylim(ax2,ax1.YLim);

ax3 = subplot(3,3,3);
mapshow(applycolourmap(G1,cmap('R1')),R);
title('Blurred Lineament Density');
set(ax3,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax3.XAxis.Exponent = 0;
xtickformat(ax3,'%.0f');

ax3.YAxis.Exponent = 0;
ytickformat(ax3,'%.0f');

ax1 = subplot(3,3,1);
mapshow(L1);
title(['Lineaments Depth ' num2str(h_sort(ind_hsort)) 'm']);
set(ax1,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax1.XAxis.Exponent = 0;
xtickformat(ax1,'%.0f');

ax1.YAxis.Exponent = 0;
ytickformat(ax1,'%.0f');
xlim(ax1,ax2.XLim);
ylim(ax1,ax2.YLim);


%% ind_Sort 8
ind_hsort = 8;

H1 = rot90(fliplr(N(:,:,ind_hsort)));
L1 = L(find(all_z==h_sort(ind_hsort)));
G1 = rot90(fliplr(G(:,:,ind_hsort)));

R = create_georasterref(bc(ind_hsort).bin_centers{1},bc(ind_hsort).bin_centers{2},size(O));

ax2 = subplot(3,3,5);
mapshow(applycolourmap(H1,cmap('R1')),R);
title('Lineament Histogram');
set(ax2,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax2.XAxis.Exponent = 0;
xtickformat(ax2,'%.0f');

ax2.YAxis.Exponent = 0;
ytickformat(ax2,'%.0f');

% xlim(ax2,ax1.XLim);
% ylim(ax2,ax1.YLim);

ax3 = subplot(3,3,6);
mapshow(applycolourmap(G1,cmap('R1')),R);
title('Blurred Lineament Density');
set(ax3,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax3.XAxis.Exponent = 0;
xtickformat(ax3,'%.0f');

ax3.YAxis.Exponent = 0;
ytickformat(ax3,'%.0f');

ax1 = subplot(3,3,4);
mapshow(L1);
title(['Lineaments Depth ' num2str(h_sort(ind_hsort)) 'm']);
set(ax1,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax1.XAxis.Exponent = 0;
xtickformat(ax1,'%.0f');

ax1.YAxis.Exponent = 0;
ytickformat(ax1,'%.0f');
xlim(ax1,ax2.XLim);
ylim(ax1,ax2.YLim);

%% ind_Sort 12
ind_hsort = 12;

H1 = rot90(fliplr(N(:,:,ind_hsort)));
L1 = L(find(all_z==h_sort(ind_hsort)));
G1 = rot90(fliplr(G(:,:,ind_hsort)));

R = create_georasterref(bc(ind_hsort).bin_centers{1},bc(ind_hsort).bin_centers{2},size(O));

ax2 = subplot(3,3,8);
mapshow(applycolourmap(H1,cmap('R1')),R);
title('Lineament Histogram');
set(ax2,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax2.XAxis.Exponent = 0;
xtickformat(ax2,'%.0f');

ax2.YAxis.Exponent = 0;
ytickformat(ax2,'%.0f');

% xlim(ax2,ax1.XLim);
% ylim(ax2,ax1.YLim);

ax3 = subplot(3,3,9);
mapshow(applycolourmap(G1,cmap('R1')),R);
title('Blurred Lineament Density');
set(ax3,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax3.XAxis.Exponent = 0;
xtickformat(ax3,'%.0f');

ax3.YAxis.Exponent = 0;
ytickformat(ax3,'%.0f');

ax1 = subplot(3,3,7);
mapshow(L1);
title(['Lineaments Depth ' num2str(h_sort(ind_hsort)) 'm']);
set(ax1,'fontsize',12);
xlabel('Easting');
ylabel('Northing');

ax1.XAxis.Exponent = 0;
xtickformat(ax1,'%.0f');

ax1.YAxis.Exponent = 0;
ytickformat(ax1,'%.0f');
xlim(ax1,ax2.XLim);
ylim(ax1,ax2.YLim);



% figure;
% imagesc(rot90(fliplr(H1)));
% ax=gca;ax.YDir='normal';
% 
% figure;
% imagesc(rot90(fliplr(G(:,:,10))));
% ax=gca;ax.YDir='normal';








function R = create_georasterref(x,y,rasterSize)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
% raster information cells
    cellsize_x  = mean(diff(x));
    cellsize_y = mean(diff(y));

    y_wlimits = [min(y)-0.5.*cellsize_y max(y)+0.5.*cellsize_y];
    x_wlimits = [min(x)-0.5.*cellsize_x max(x)+0.5.*cellsize_x];

    R = maprasterref('RasterSize', rasterSize, ...
              'YWorldLimits', y_wlimits, 'ColumnsStartFrom','south', ...
              'XWorldLimits', x_wlimits);
end