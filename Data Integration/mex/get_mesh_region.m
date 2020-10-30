function [F2,V2,v_ids] = get_mesh_region(F,V,face_ids)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    F_s = F(face_ids,:);
    v_ids = unique(F_s(:));
    V2 = V(v_ids,:);
    F2 = [];
    
    [~, idx_loc] = ismember(F_s(:,1), v_ids);
    F2(:,1)= idx_loc;
    [~, idy_loc] = ismember(F_s(:,2), v_ids);
    F2(:,2)= idy_loc;
    [~, idz_loc] = ismember(F_s(:,3), v_ids);
    F2(:,3)= idz_loc;

end

