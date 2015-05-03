from klustakwik2 import *
from pylab import *
import time
import cPickle as pickle
import os
from random import sample
import shutil

if __name__=='__main__':
    
    fname, shank = '../temp/testsmallish', 4
    #fname, shank = '../temp/20141009_all_AdjGraph', 1
    
    log_to_file(fname+'.klg.'+str(shank), 'debug')
    log_suppress_hierarchy('klustakwik', inclusive=False)
    
    if os.path.exists(fname+'.pickle'):
#     if False:
        start_time = time.time()
        data = pickle.load(open(fname+'.pickle', 'rb'))
        print 'load from pickle:', time.time()-start_time
    else:
        start_time = time.time()
        raw_data = load_fet_fmask_to_raw(fname, shank, drop_last_n_features=1)
        print 'load_fet_fmask_to_raw:', time.time()-start_time
        data = raw_data.to_sparse_data()
        pickle.dump(data, open(fname+'.pickle', 'wb'), -1)
        
    print 'Number of spikes:', data.num_spikes
    print 'Number of unique masks:', data.num_masks
    
    kk = KK(data, max_iterations=1000,
#             split_every=1, split_first=1, # for debugging splits
#             split_every=1000000, split_first=1000000, # disable splitting
#             points_for_cluster_mask=1000, # don't use reduced cluster masks
            )
#     kk.register_callback(SaveCluEvery(fname, shank, every=10))
    kk.register_callback(MonitoringServer())
    
#     dump_covariance_matrices(kk)
#     dump_cluster_counts(kk)
#     dump_cluster_counts(kk, slot='end_M_step')
#     dump_cluster_counts(kk, slot='start_M_step')
#     dump_cluster_means(kk)
    
    def printclu_before(kk):
        global clu_here
        clu_here = kk.clusters.copy()
    def printclu_after(kk):
        changed = (kk.clusters!=clu_here).nonzero()[0]
        print 'Changed:', changed
        print kk.old_clusters[changed]
        print kk.clusters[changed]
#     kk.register_callback(printclu_before, 'start_EC_steps')
#     kk.register_callback(printclu_after, 'end_EC_steps')
    
    if os.path.exists(fname+'.clu.'+str(shank)+'.flipflop'):
#     if False:
        shutil.copy(fname+'.clu.'+str(shank)+'.flipflop', fname+'.clu.'+str(shank))
#     if os.path.exists(fname+'.clu.'+str(shank)):
    if False:
        print 'Loading clusters from file'
        clusters = loadtxt(fname+'.clu.'+str(shank), skiprows=1, dtype=int)
        kk.cluster_from(clusters)
    else:
        print 'Generating clusters from scratch'
        kk.cluster(100)
    save_clu(kk, fname, shank)
    
    clusters = kk.clusters
    kk.reindex_clusters()
    
    num_to_show = 200
     
    for cluster in xrange(kk.num_clusters_alive):
        if cluster % 4 == 0:
            figure()
        maskimg = []
        spikes = kk.get_spikes_in_cluster(cluster)
        if len(spikes)>num_to_show:
            spikes = sample(spikes, num_to_show)
        for spike in spikes:
            row = zeros(kk.num_features)
            unmasked = data.unmasked[data.unmasked_start[spike]:data.unmasked_end[spike]]
            row[unmasked] = data.masks[data.values_start[spike]:data.values_end[spike]]
            maskimg.append(row)
        if len(maskimg)==0:
            continue
        maskimg = array(maskimg)
        subplot(2, 2, cluster%4 + 1)
        imshow(maskimg, origin='lower left', aspect='auto', interpolation='nearest')
        gray()
        title(cluster)
    show()
