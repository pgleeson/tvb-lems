from neuromllite import Network, Cell, InputSource, Population, Synapse, RectangularRegion, RandomLayout
from neuromllite import Projection, RandomConnectivity, OneToOneConnector, Input, Simulation

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite.sweep.ParameterSweep import *

import sys


def generate():
    ################################################################################
    ###   Build new network

    net = Network(id='ExampleK')
    net.notes = 'Example...'

    net.parameters = { 'pop_size':       '8' ,
                       'stim_amp':       '0.3'}

    cell = Cell(id='kuramoto1', lems_source_file='CellExamples.xml')


    net.cells.append(cell)



    input_source = InputSource(id='iclamp0', 
                               neuroml2_input='PulseGeneratorDL', 
                               parameters={'amplitude':'stim_amp', 'delay':'100ms', 'duration':'800ms'})
    net.input_sources.append(input_source)
    '''

    input_source = InputSource(id='poissonFiringSyn', 
                               neuroml2_input='poissonFiringSynapse',
                               parameters={'average_rate':"eta", 'synapse':"ampa", 'spike_target':"./ampa"})


'''

    r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    net.regions.append(r1)

    pE = Population(id='Epop', 
                    size='pop_size', 
                    component=cell.id, 
                    properties={'color':'1 0 0'},
                    random_layout = RandomLayout(region=r1.id))
    
    net.populations.append(pE)

    '''
    net.synapses.append(Synapse(id='ampa', 
                                pynn_receptor_type='excitatory', 
                                pynn_synapse_type='curr_alpha', 
                                parameters={'tau_syn':0.1}))


    net.projections.append(Projection(id='projEinput',
                                      presynaptic=pEpoisson.id, 
                                      postsynaptic=pE.id,
                                      synapse='ampa',
                                      delay=2,
                                      weight=0.02,
                                      one_to_one_connector=OneToOneConnector()))
               
    net.projections.append(Projection(id='projEE',
                                      presynaptic=pE.id, 
                                      postsynaptic=pE.id,
                                      synapse='ampa',
                                      delay=2,
                                      weight=0.002,
                                      random_connectivity=RandomConnectivity(probability=.5)))

    net.projections.append(Projection(id='projEI',
                                      presynaptic=pE.id, 
                                      postsynaptic=pI.id,
                                      synapse='ampa',
                                      delay=2,
                                      weight=0.02,
                                      random_connectivity=RandomConnectivity(probability=.5)))
    
    net.projections.append(Projection(id='projIE',
                                      presynaptic=pI.id, 
                                      postsynaptic=pE.id,
                                      synapse='gaba',
                                      delay=2,
                                      weight=0.02,
                                      random_connectivity=RandomConnectivity(probability=.5)))
    '''
    net.inputs.append(Input(id='stim',
                            input_source=input_source.id,
                            population=pE.id,
                            percentage=50))

    #print(net)
    #print(net.to_json())
    new_file = net.to_json_file('%s.json'%net.id)


    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='SimExampleK',
                     network=new_file,
                     duration='1000',
                     dt='0.025',
                     seed= 123,
                     recordVariables={'sin_theta':{pE.id:'*'}})

    sim.to_json_file()
    
    return sim, net



if __name__ == "__main__":

    if '-sweep' in sys.argv:
        
        sim, net = generate()
        
        fixed = {'dt':0.001, 'order':1}
 
        #
        vary = {'eta':[0.5,1,1.5,2,10]}
        #vary = {'eta':[1,2]}
        #vary = {'eta':[1]}
        #vary = {'eta':[i/1000. for i in xrange(0,200,20)]}
        #vary = {'stim_amp':['1.5pA']}
        
        vary['seed'] = [i for i in range(30)]

        simulator = 'jNeuroML'
        simulator = 'PyNN_NEST'
        simulator = 'jNeuroML'
        simulator = 'jNeuroML_NetPyNE'
        simulator = 'jNeuroML_NEURON'

        nmllr = NeuroMLliteRunner('SimExample7.json',
                                  simulator=simulator)

        ps = ParameterSweep(nmllr, 
                            vary, 
                            fixed,
                            num_parallel_runs=16,
                            plot_all=False, 
                            heatmap_all=False,
                            show_plot_already=False,
                            peak_threshold=0)

        report = ps.run()
        ps.print_report()

        #  ps.plotLines('weightInput','average_last_1percent',save_figure_to='average_last_1percent.png')
        #ps.plotLines('weightInput','mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        #ps.plotLines('eta','Einput[0]/spike:mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        ps.plotLines('eta','Einput[0]/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_ein.png')
        ps.plotLines('eta','Epop[0]/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_e.png')
        ps.plotLines('eta','Ipop[0]/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_i.png')

        import matplotlib.pyplot as plt

        plt.show()
    
    else:

        sim, net = generate()

        ################################################################################
        ###   Run in some simulators

        import sys

        check_to_generate_or_run(sys.argv, sim)

