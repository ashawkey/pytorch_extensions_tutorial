import torch
import torch.nn as nn

import modules.functional as F


class AvgVoxelization(nn.Module):
    def __init__(self, resolution, normalize=True, eps=1e-6):
        super().__init__()
        self.r = int(resolution)
        self.normalize = normalize
        self.eps = eps

    def forward(self, features, coords):
        coords = coords.detach()

        # normalize and clamp coords, then round to int [0, r-1]
        norm_coords = coords - coords.mean(2, keepdim=True)
        if self.normalize:
            norm_coords = norm_coords / (norm_coords.norm(dim=1, keepdim=True).max(dim=2, keepdim=True).values * 2.0 + self.eps) + 0.5
        else:
            norm_coords = (norm_coords + 1) / 2.0
        norm_coords = torch.clamp(norm_coords * self.r, 0, self.r - 1)

        vox_coords = torch.round(norm_coords).to(torch.int32)
        return F.avg_voxelize(features, vox_coords, self.r), norm_coords

    def extra_repr(self):
        return 'resolution={}{}'.format(self.r, ', normalized eps = {}'.format(self.eps) if self.normalize else '')



class TrilinearVoxelization(nn.Module):
    def __init__(self, resolution, normalize=True, eps=1e-6):
        super().__init__()
        self.r = int(resolution)
        self.normalize = normalize
        self.eps = eps

    def forward(self, features, coords):
        coords = coords.detach()

        # normalize and clamp coords, then round to int [0, r-1]
        norm_coords = coords - coords.mean(2, keepdim=True)
        if self.normalize:
            norm_coords = norm_coords / (norm_coords.norm(dim=1, keepdim=True).max(dim=2, keepdim=True).values * 2.0 + self.eps) + 0.5
        else:
            norm_coords = (norm_coords + 1) / 2.0

        # do not round to int ! just clamp to [0, r)
        # FIXME ? only clamp to [0, r-1] works, else will cause illegal memory access. maybe a potential bug!
        norm_coords = torch.clamp(norm_coords * self.r, 0, self.r - 1)
        

        return F.trilinear_voxelize(features, norm_coords, self.r), norm_coords

    def extra_repr(self):
        return 'resolution={}{}'.format(self.r, ', normalized eps = {}'.format(self.eps) if self.normalize else '')