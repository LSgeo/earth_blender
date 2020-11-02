function [F,V,vidx_out] = get_mesh_region_vf_conn(V,F,region)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

face_ids = ismember(F(:,1),find(~region)) |...
           ismember(F(:,2),find(~region)) |...
           ismember(F(:,3),find(~region));

F_all = F;
V_all = V;

[F,V,vids] = get_mesh_region(F_all,V_all,face_ids);
% [comps_v,comps_f] = connected_components([F;repmat(size(V,1),1,3)]);
% vert_idxs = find(comps_v==1);
% if(numel(unique(comps_v))>1)
%     [F,V] = get_mesh_region_byverts(F,V,vert_idxs);
% end
% 
% vidx_out = vids(vert_idxs);
vidx_out = vids;
end
