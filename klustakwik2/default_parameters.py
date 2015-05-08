'''
Default clustering parameters
'''

from numpy import log

default_parameters = dict(
     prior_point=1,
     mua_point=2,
     noise_point=1,
     points_for_cluster_mask=100,
     penalty_k=0.0,
     penalty_k_log_n=1.0,
     max_iterations=1000,
     num_changed_threshold=0.05,
     full_step_every=20,
     split_first=20,
     split_every=40,
     max_possible_clusters=1000,
     mask_starts=500,
     dist_thresh=log(1000.0),
     max_quick_step_candidates=100000000, # this uses around 760 MB RAM
     always_split_bimodal=False,
     )
