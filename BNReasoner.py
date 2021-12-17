from typing import Union
from BayesNet import BayesNet
import pandas as pd
import numpy as np
from itertools import compress, product

class BNReasoner:
    def __init__(self, net: Union[str, BayesNet]):
        """
        :param net: either file path of the bayesian network in BIFXML format or BayesNet object
        """
        if type(net) == str:
            # constructs a BN object
            self.bn = BayesNet()
            # Loads the BN from an BIFXML file
            self.bn.load_from_bifxml(net)
        else:
            self.bn = net

    def get_bn(self):
        return self.bn

    def get_children_from_set_vars(self,vars_set):
        aux = []
        for var in vars_set:
            aux.append(self.bn.get_children(var))
        children_of_set  = [val for sublist in aux for val in sublist]
        children_of_set = list(set(children_of_set))
        return children_of_set

    def d_separator(self, X, Z, Y):
        '''Given 3 sets of variables X, Y , and Z,
        determine whether X is independent of Y given Z'''

        answer="False - Z does not d-separate X from Y"
        all_children_of_X = self.get_children_from_set_vars(X) 
        all_children_of_Z = self.get_children_from_set_vars(Z) 
        all_children_of_Y = self.get_children_from_set_vars(Y) 
        
        '''Squential Valve  X-> Z-> Y '''
        #if any ele in X is a parent of an ele in Z
        if any(elem in all_children_of_X for elem in Z):
            #if any ele in Z is a parent of an ele in Y
            if any(elem in all_children_of_Z for elem in Y):
                #then they have Squential VALVE
                #So X is d-separated to Y, by Z
                answer="True - Z d-separates X from Y with SQUENTIAL VALVE"

        '''Divergent Valve  X <-Z-> Y '''
        if any(elem in all_children_of_Z for elem in X):
            if any(elem in all_children_of_Z for elem in Y):
                answer="True - Z d-separates X from Y with DIVERGENT VALVE"

        '''Convergent Valve  X-> Z <-Y  '''
        if any(elem in all_children_of_X for elem in Z):
            if any(elem in all_children_of_Y for elem in Z):
                answer="True - Z d-separates X from Y with CONVERGENT VALVE"
        return answer

    
    def compute_elimination_order(self,X):
        '''Ordering: Given a set of variables X in the Bayesian network, compute a good ordering for
        elimination of X based on the min-degree heuristics and the min-fill heuristics '''
        I_graph = self.bn.get_interaction_graph()
        elimination_order = []


        neighbor_map={key: None for key in X}
        for node in neighbor_map:
            node_neighbors = [neighbor for neighbor in I_graph.neighbors(node)]
            neighbor_map[node]=len(node_neighbors)
            
        elimination_order.append(min(neighbor_map, key=neighbor_map.get))

        
        return

    def create_empty_f(self, X):
        X.append('p')
        df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=['a', 'b', 'c'])


    def multiplication(self,factor1,factor2):
        factors_list=[factor1,factor2]
        f_vars = []
        small_f_vars = []

        if factor1.size > factor2.size:
            f=factor1
            small_f=factor2
        else:
            f=factor2
            small_f=factor2
        
        f_vars.append(list(factor1.columns))
        small_f_vars.append(list(factor2.columns))
        
        all_vars = [item for sublist in f_vars+small_f_vars for item in sublist if item != 'p']
        all_vars= list(set(all_vars))

        #!assuming every vaule will have the same values!
        vars_values=list(set(factor1[all_vars[0]]))
        #print('vars_values',vars_values)

        all_value_combinations=list(product(*[vars_values]*len(all_vars)))
        new_factor = pd.DataFrame(all_value_combinations, columns = all_vars)
        new_factor['p'] = float(1)
        
        
        for index, row in new_factor.iterrows():
            #rowrow.index.tolist()
            instantiation = row[:-1]
            to_multiply=[]

            for f in factors_list:
                aux=self.bn.get_compatible_instantiations_table(instantiation,f)
                to_multiply.append(aux['p'].sum())
                
            new_factor.at[index,'p']=np.prod(to_multiply)

        return new_factor

                


                

                


                
      

    #Marginalizing
    def summing_out(self, factor_of_X, Z):
        '''Z = set of vars to eliminate;  factor_of_X = the CPT table from where Z is gonna be removed'''
        X=list(factor_of_X.columns)
        X=X[:-1]
        #Y=X-Z
        Y=[var for var in X if var not in Z]
  
        '''Creating an empty factor'''
        new_factor = factor_of_X.drop(Z, axis = 1)
        new_factor['p'] = new_factor['p']*0

        for i, row in new_factor.iterrows():
            for j,row_to_compare in new_factor.drop(index=i).iterrows():
                if row.to_string(index=False) == row_to_compare.to_string(index=False):
                    new_factor.loc[i,'p']=factor_of_X.iloc[i]['p']+factor_of_X.iloc[j]['p']

        new_factor.drop(new_factor[(new_factor['p'] ==0)].index, inplace=True)
        return new_factor
        
       
        
      

    def compute_marginal_distribution(self, Q, E):
        '''Given query variables Q and a possibly empty evidence E,
        Computes the marginal distribution P (Q|E)'''
        self.network_pruning(Q, E)


    





    def network_pruning(self, Q, E):
        '''Given a set of query variables Q and evidence E, node- and edge-prune the
        Bayesian network s.t. queries of the form P (Q|E) can still be correctly calculated'''
        self.node_pruning(Q, E)
        self.edge_pruning(E, pd.Series({'Winter?': True, 'Rain?': False}))

    def are_connected(self,node, neighbor):
        if node in self.bn.get_children(neighbor) or neighbor in self.bn.get_children(node):
            return True
        else: return False

    def node_pruning(self, Q, E):

        I_graph = self.bn.get_interaction_graph()
        nodes_to_remove=[]
        for node in I_graph:
            node_neighbors = [neighbor for neighbor in I_graph.neighbors(node) if self.are_connected(node,neighbor)]                
            #print('Node ', node, ' number of neighbors ',node_neighbors)
            if len(node_neighbors)<=1:
            # 'node' is a LEAF NODE
                if node not in Q and node not in E:
                # and 'node' is not a relevant to answer the query (Q,E), so Remove 'node'
                    print(node)
                    nodes_to_remove.append(node)
        #Pruning (deleting all the LEAF NODES)         
        for node in nodes_to_remove:
            self.bn.del_var(node)

    def edge_pruning(self, E, E_instantiation : pd.Series):
        '''E= Evidence Vars. This list will be removed from the BN'''
        #print(self.bn.draw_structure())
        for evidence_var in E:
            for var in self.bn.get_all_variables():
                if self.are_connected(evidence_var,var):
                #Remove all the edges from the 'evidence_var'
                    self.bn.del_edge((evidence_var,var))
                    cpt=self.bn.get_cpt(var)
                    if evidence_var in cpt:
                        new=self.bn.reduce_factor(E_instantiation, cpt)
                        new.drop(new[new['p'] == '_'].index, inplace=True)
                        new.drop([evidence_var], axis=1, inplace=True)
                        self.bn.update_cpt(var,new)
                    print(self.bn.get_cpt(var))
                      

        
        

        #Sum up the evidence contradictions from every CPT
         
        #Update the CPT tables 

                




        