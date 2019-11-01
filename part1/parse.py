import argparse

# Override ArgumentParser to read not only line by line
class MyArgumentParser(argparse.ArgumentParser):
    def convert_arg_line_to_args(self, arg_line):
        return arg_line.split()

class ParseThings:

    # Define parser
    def __init__(self):   
        self.parser = MyArgumentParser(fromfile_prefix_chars='@')

        # Define arguments
        self.parser.add_argument('--comment', nargs='*', help='Comment in file')
        self.parser.add_argument('--line', dest='lines', nargs=3, action='append', type=float,
            help='Add spectrum line with Energy, Intensity and deltaE(FWHM)')
        self.parser.add_argument('--background', dest='background', nargs=4, type=float, default = [1., 2., 3., 4.],
            help='background parameters: par[0] * exp( par[1] * x) + par[2] + par[3] * x')
        self.parser.add_argument('--E_max', dest='e_max', type=float, help='Define maximal spectrum energy', default=1.)
        self.parser.add_argument('--chanels', dest='chanels_num', type=int, help='Number of chanels', default=1000)
        self.parser.add_argument('--E0', dest='E0', type=float, help='Energy shift', default=0.01)
        self.parser.add_argument('--time', dest='time', type=float, help='Time', default=100)
        self.parser.add_argument('--background_intensity', dest='background_intensity', type=float, help='Intensity of background', default=10)

    # Parse things method
    def parse(self):
        return self.parser.parse_args()