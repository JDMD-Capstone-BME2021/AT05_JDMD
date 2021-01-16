class ReconstructionOptions:

    def __init__(self, method='fbp', nthreads=1, start_angle=0.0, end_angle=180.0, fbp_filter='ramp',
                 fbp_interpolations='linear', sart_iterations=1, sart_relaxation=0.15):
        if method == 'fbp' or method == 'sart':
            self.method = method
        else:
            print('[WARNING] Reconstruction method set to \'' + method
                  + '\' expected \'fbp\' or \'sart\'. Setting to \'fbp\'.')
            self.method = 'fbp'

        if nthreads > 0:
            self.nthreads = nthreads
        else:
            print('[WARNING] Reconstruction number of threads set to ' + str(nthreads)
                  + ' expected 1 or greater. Setting to 1.')

        if start_angle < 0:
            print('[WANRING] Reconstruction start angle set to ' + str(start_angle)
                  + ' expected non-negative. Setting to 0.0')
            self.start_angle = 0.0
        else:
            self.start_angle = start_angle

        if end_angle < 0:
            print('[WANRING] Reconstruction end angle set to ' + str(start_angle)
                  + ' expected non-negative. Setting to 0.0')
            self.end_angle = 0.0
        elif end_angle <= self.start_angle:
            print('[WARNING] Reconstruciton end angle set to ' + str(end_angle)
                  + ' expected end angle to be greated than start angle. Setting to ' + str(self.start_angle + 180))
            self.end_angle = self.start_angle
        else:
            self.end_angle = end_angle

        # todo: add verification for other parameters
        self.fbp_filter = fbp_filter
        self.fbp_interpolation = fbp_interpolations
        self.sart_iterations = sart_iterations
        self.sart_relaxation = sart_relaxation


class ImgLoadOptions:

    def __init__(self, input_dir, resolution, padding):
        self.input_dir = input_dir
        self.resolution = resolution
        self.padding = padding
