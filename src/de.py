"""
Implements the differential evolution optimization method by Storn & Price
(Storn, R., Price, K., Journal of Global Optimization 11: 341--359, 1997)

.. moduleauthor:: Hannu Parviainen <hannu@iac.es>
"""
import sys
import numpy as np
from numpy import asarray, tile
from numpy.random import seed, random, randint

class DiffEvol(object):
    """
    Implements the differential evolution optimization method by Storn & Price
    (Storn, R., Price, K., Journal of Global Optimization 11: 341--359, 1997)
    """
    def __init__(self, fun, bounds, npop, ngen, F=0.5, C=0.5, seed=0, verbose=True):
        """

        :param fun: the function to be minimized
        :param bounds: parameter bounds as [npar,2] array
        :param npop:   the size of the population (5*D - 10*D)
        :param  ngen:  the number of generations to run
        :param  F:     the difference amplification factor. Values of 0.5-0.8 are good
                       in most cases.
        :param C:      The cross-over probability. Use 0.9 to test for fast convergence,
                       and smaller values (~0.1) for a more elaborate search.
        
        N free parameters
        N population vectors (pv1 .. pvN)
        
        Population = [pv1_x1 pv1_x2 pv1_x3 ... pv1_xN]
                     [pv2_x1 pv2_x2 pv2_x3 ... pv2_xN]
                     .
                     .
                     .
                     [pvN_x1 pvN_x2 pvN_x3 ... pvN_xN]
        
        Population = [pv, parameter]
        """ 
        self.minfun = fun
        self.bounds = asarray(bounds)
        self.n_gen  = ngen
        self.n_pop  = npop
        self.n_parm = (self.bounds).shape[0]
        self.bl = tile(self.bounds[:,0],[npop,1])
        self.bw = tile(self.bounds[:,1]-self.bounds[:,0],[npop,1])
        
        self.seed = seed
        self.F = F
        self.C = C
        self.verbose = verbose

        np.random.seed(self.seed)
        self.result = DiffEvolResult(npop, self.n_parm, self.bl, self.bw)


    def __call__(self):
        """The differential evolution algorithm.
           Note: here we maximize the function instead of minimizing."""
        r = self.result
        t = np.zeros(3, np.int)
        
        for i in xrange(self.n_pop):
            r.fit[i] = self.minfun(r.pop[i,:])
            
        for j in xrange(self.n_gen):
            for i in xrange(self.n_pop):
                t[:] = i
                while  t[0] == i:
                    t[0] = randint(self.n_pop)
                while  t[1] == i or t[1] == t[0]:
                    t[1] = randint(self.n_pop)
                while  t[2] == i or t[2] == t[0] or t[2] == t[1]:
                    t[2] = randint(self.n_pop)
    
                v = r.pop[t[0],:] + self.F * (r.pop[t[1],:] - r.pop[t[2],:])

                ## --- CROSS OVER ---
                crossover = random(self.n_parm) <= self.C
                u = np.where(crossover, v, r.pop[i,:])

                ## --- FORCED CROSSING ---
                ri = randint(self.n_parm)
                u[ri] = v[ri].copy()

                ufit = self.minfun(u)
    
                if ufit < r.fitness[i]:
                    r.pop[i,:] = u[:].copy()
                    r.fit[i]   = ufit
                          
            if self.verbose:
                sys.stdout.write('\rNode %i finished generation %4i/%4i  F = %7.5f'%(self.rank, j+1, self.n_gen, r.fit.min())); sys.stdout.flush()

        self.result.minidx = np.argmin(r.fitness)
        return self.result


class DiffEvolResult(object):
    """
    Encapsulates the results from the differential evolution fitting.
    """
    def __init__(self, npop, npar, bl, bw):
        self.population = bl + random([npop, npar]) * bw
        self.fitness    = np.zeros(npop)
        self.pop        = self.population
        self.fit        = self.fitness
        self.minidx     = None

        
    def get_fitness(self):
        """Returns the best-fit value of the minimized function."""
        return self.fitness[self.minidx]

    
    def get_best_fit(self):
        """Returns the best-fit solution."""
        return self.population[self.minidx,:]
