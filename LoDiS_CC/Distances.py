import numpy as np
from ase.io import read
from quantity import Quantity


class Positions(Quantity):
    name = 'pos'
    display_name = 'Positions'
    number = '1'

    def __init__(self, system, metadata):
        self.file = read(system[''], index = ':')
        self.DataSet = [atoms.get_positions() for atoms in self.file]
        
    def calculate(self, i_frame, result_cache, metadata):
        return self.DataSet[i_frame]
    
    def get_dimensions(self, n_atoms, n_elements):
        return n_atoms, 3, np.float
    
    def cleanup(self):
        pass

class Elements(Quantity):
    name = 'ele'
    display_name = 'Elements'
    number = '2'
    
    def __init__(self, system, metadata):
        self.file = read(system[''], index= ':')
        self.DataSet = [atoms.get_chemical_symbols() for atoms in self.file]
    
    def calculate(self, i_frame, result_cache, metadata):
        return self.DataSet[i_frame]
    
    def get_dimensions(self, n_atoms, n_elements):
        return n_atoms, 1, np.float
    
    def cleanup(self):
        pass

class Euc_Dist(Quantity):
    name = 'euc'
    display_name = 'Euclidean_Distance'
    number = '3'
    dependencies = [Positions]
    
    def calculate(self, i_frame, result_cache, metadata):
        positions = result_cache[Positions]
        Distances=[]
        for i in range(len(positions)-1):
            for j in range(i+1,len(positions)):
                Euc=(positions[i,0]-positions[j,0])**2
                +(positions[i,1]-positions[j,1])**2
                +(positions[i,2]-positions[j,2])**2

                Distances.append(np.sqrt(Euc))
        return Distances
    
    def get_dimensions(self, n_atoms, n_elements):
        return self.n_atoms * (self.n_elements - 1) / 2 , np.float
    
class MetA_MetA(Quantity):
    name = 'm1_m1'
    display_name = 'Homo_Pair_Distances'
    number = '4'
    dependencies = [Positions, Elements]
    
    def not_found_string(self):
        return "Sorry, but that species is not present."
    
    def select_species(self, result_cache, metadata):
        elements = set(result_cache[Elements])
        print("Present species are " + x for x in elements)
        specie = input("Please select the chemical species for examination from the above list.")
        if specie not in elements:
            raise NameError(self.not_found_string)
    
    def calculate(self, i_frame, result_cache, metadata, specie):
        positions = result_cache[Positions]
        elements = result_cache[Elements]
        Distances=[]; Temp=np.array(np.delete(Vector, (0),axis=1), dtype=np.float64)
        for i in range(len(Vector)-1):
            for j in range(i+1,len(Vector)):
                if Vector[i,0]==Species and Vector[j,0]==Species:
                    Euc=(Temp[i,0]-Temp[j,0])**2+(Temp[i,1]-Temp[j,1])**2+(Temp[i,2]-Temp[j,2])**2
                    Distances.append(np.sqrt(Euc))
        return Distances
        

class Distance():

    def __init__(self, distances, species):
        
        self.distances = distances
        
        self.species = species
    """ Robert
    This class of functions is designed to extract information regarding atomic positions
    for a whole trajectory and generate data regarding spatial distributions of all, homo, and
    hetero combinations. 
    """
        
    def Euc_Dist(Vector):
        
        """ Robert
        Vector: The tensor containing the xyz coordinates of all atoms in a given trajectory.
        This function will only act on one frame at any given time but can be iteratively 
        called so at to generate information regarding specific frames of a simulation.
        
        This is generally expected to be the output of "read_trajectory" in the 
        "Movie_Read.py" module which generates the xyz coordinates as well as the 
        numbered list of elements. These are initially kept separate although there
        does exist provision to stack these tensors to facilitate the homo/hereo 
        PDDFs.
        
        This function is indiscriminate regarding chemical species. It will calculate 
        pair-wise distances regardless of chemical species and return a 1D numpy array
        of all possible pairwise distances which is N!(N-1)!/2
        So bear in mind that this function scales poorly with system size!
        """
        
        Number = '1'
        
        Distances=[]; Temp=np.array(np.delete(Vector, (0),axis=1), dtype=np.float64)
        for i in range(len(Vector)-1):
            for j in range(i+1,len(Vector)):
                Euc=(Temp[i,0]-Temp[j,0])**2+(Temp[i,1]-Temp[j,1])**2+(Temp[i,2]-Temp[j,2])**2

                Distances.append(np.sqrt(Euc))
        return Distances




    
    def M1_M1(Vector,Species):
        
        """ Robert
        
        Vector: The tensor containing the xyz coordinates of all atoms in a given trajectory.
        This function will only act on one frame at any given time but can be iteratively 
        called so at to generate information regarding specific frames of a simulation.
        
        Species: The chemical symbol for the element to be considered. Parameter expected 
        to be input as such
        
        "M1_M1(Positions, Au)" if one were to analyse the xyz trajectory and was interested only 
        in gold.
        
        This function has near identical architecture to the one defined above, "Euc_Dist",
        with the exception that the function actively searches for similar chemical species
        from the input trajectory.
        """
        
        Number = '2'
        
        Distances=[]; Temp=np.array(np.delete(Vector, (0),axis=1), dtype=np.float64)
        for i in range(len(Vector)-1):
            for j in range(i+1,len(Vector)):
                if Vector[i,0]==Species and Vector[j,0]==Species:
                    Euc=(Temp[i,0]-Temp[j,0])**2+(Temp[i,1]-Temp[j,1])**2+(Temp[i,2]-Temp[j,2])**2
                    Distances.append(np.sqrt(Euc))
        return Distances

    
    def M1_M2(Vector):
        
        """ Robert
        
        Vector: The tensor containing the xyz coordinates of all atoms in a given trajectory.
        This function will only act on one frame at any given time but can be iteratively 
        called so at to generate information regarding specific frames of a simulation.
        
        Note that no species need to be defined for this function as it is understood that LoDiS
        only has provision for mono/bimetallic systems (for the time being) although this
        function could be further generalised (albeit it a potential cost to computation time).
        """
        
        Number ='3'
        
        Distances=[]; Temp=np.array(np.delete(Vector, (0),axis=1), dtype=np.float64)
        for i in range(len(Vector)-1):
            for j in range(i+1,len(Vector)):
                if Vector[i,0]!=Vector[j,0]:
                    Euc=(Temp[i,0]-Temp[j,0])**2+(Temp[i,1]-Temp[j,1])**2+(Temp[i,2]-Temp[j,2])**2
                    Distances.append(np.sqrt(Euc))

        return Distances
    
def get_cutoff_distance(distances, r_cut):
    
    """ Robert
    
    distances: A numpy array containing the unsorted list of calculated pair 
    distances as calculated by a given function in the Distances class.
    
    r_cut: An initial estimate for the nearest neighbour distance. Without loss
    of gnerality, one may set this to be the maximum distance as found in the 
    above function. Naturally this comes with a computational price.
    
    Function returns an estimate for the optimal r_cut value by searching for the 
    first local minimum of the PDDF.
    
    Code contributed by Matteo.
    """
    
    Number = '4'
    
    
    
    y, bin_edges = np.histogram(distances, bins = np.linspace(0, r_cut, r_cut*100+1))
    x = bin_edges[:-1] + 0.005
    y = np.array(y) / sum(np.array(y))
    x = np.asarray(x)
    minima = []
    for i in range(len(y)-10):
        if y[i] < y[i+10] and y[i] < y[i-10]:
            minima.append(x[i])
    r_cut_cn = minima[0]
    return r_cut_cn
                
                

if __name__ == '__main__':
    import Movie_Read as Read

    Energy, Trajectory, Elements=Read.Manual_Input()
    Positions=[];Distances=[]

    for x in range(11000):
        Positions.append(np.column_stack((Elements[x],Trajectory[x])))
        Distances.append(Distance.Euc_Dist(Positions[x]))   #All possible pairings