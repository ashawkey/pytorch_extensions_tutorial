#ifndef _VOX_CUH
#define _VOX_CUH

// CUDA function declarations
void avg_voxelize(int b, int c, int n, int r, int r2, int r3, const int *coords,
                  const float *feat, int *ind, int *cnt, float *out);

void avg_voxelize_grad(int b, int c, int n, int s, const int *idx,
                       const int *cnt, const float *grad_y, float *grad_x);

void trilinear_voxelize(int b, int c, int n, int r, int r2, int r3, 
                        const float *coords, const float *feat, 
                        int *inds, float *wgts, int *cnt, float *out);

void trilinear_voxelize_grad(int b, int c, int n, int s, 
                        const int *inds, const float *wgts, const int *cnt, 
                        const float *grad_y, float *grad_x);

#endif
