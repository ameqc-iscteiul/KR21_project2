from typing import Union
from BayesNet import BayesNet
from BNReasoner import BNReasoner
import pandas as pd

def main():
    net = BayesNet()
    net.load_from_bifxml("C:/Users/ASUS/Vs_workspace/VU/KR/project_2/KR21_project2/testing/testt.BIFXML")
    #print("net.get_all_variables()",net.get_all_variables())
    #reasoner = BNReasoner(net)
    
    net.draw_structure()
    #reasoner.network_pruning('Wet Grass?',['Winter?','Rain?'])
    #net.draw_structure()

    vars = net.get_all_variables()
    cpt=net.get_cpt(vars[2])
    cpt2=net.get_cpt(vars[1])
    '''print(net.get_cpt(vars[0]))
    print(net.get_cpt(vars[1]))
    print(net.get_cpt(vars[2]))
    print(net.get_cpt(vars[3]))
    print(net.get_cpt(vars[4]))
    '''
    print('cpt',cpt)
    print('cpt2',cpt2)

    print('muultiplication')
    res = reasoner.multiplication(cpt,cpt2)
    print(res)

    '''
    new_cpt = cpt.drop(vars[0], axis='columns')
    print(new_cpt)
    
    rows = new_cpt.iterrows()
    f=0
    t=0
    for data in rows:
        sub=data[1]
        print('sub[vars[2]]',sub[vars[2]])
        if sub[vars[2]]==False:
            print("sub['p']",sub['p'])
            f=f+sub['p']
        else: 
            print("sub['p']",sub['p'])
            t=t+sub['p']

    print("f",f,"t",t)
    new_cpt.loc[new_cpt['Rain?'] == False, 'p'] = f
    new_cpt.loc[new_cpt['Rain?'] == True, 'p'] = t
    new_cpt.drop_duplicates(inplace=True)

    print(new_cpt)

    #net.update_cpt(vars(2), new_cpt)
    #print(net.get_cpt(vars(2)))


    print (r.d_separator(['Wet Grass?'],['Sprinkler?'],['Winter?']))
    print (r.d_separator(['Winter?'],['Sprinkler?'],['Wet Grass?']))

    print (r.d_separator(['Sprinkler?'],['Winter?'],['Rain?']))
    print (r.d_separator(['Wet Grass?'],['Rain?'],['Slippery Road?']))

    print (r.d_separator(['Sprinkler?'],['Wet Grass?'],['Rain?']))

    print (r.d_separator(['Rain?'],['Winter?'],['Wet Grass?']))
    print (r.d_separator(['Rain?'],['Slippery Road?'],['Wet Grass?']))
'''




if __name__ == '__main__':
    main()

    # TODO: This is where your methods should go