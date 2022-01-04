
#initializing the constant and directory path

thumbnail_dir = "static/thumbnail_img/y{}/"
thumbnail_url = "MST3uvw/static/thumbnail_img/y{}/{}"

dname = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min"
rti_gg_files = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min/{}/Maps/fitmap_{}.{}.{}.npz"
wind_files = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min/{}/Maps/windmap2_{}.{}.{}.npz"

specs_dir = "/rd2/MST_ISR_EEJ_cont/processed/MST/spc/y{}/spc1min/{}.{}.{}/"

t_min = 6
t_max = 19
h_min = 60 - .15/2 #Offset for accuracy
h_max = 89.7 + .15/2 #Offset for accuracy and maxed at 89.7 for UVW(2 less pts than RTI)


colors = ['RdBu', 'plasma', 'viridis', 'gray', 'jet', 'RdBu_r']

#slider range endpoints
rti_low = -18
rti_high = 10
u_low = -80
u_high = 80
v_low = -100
v_high = 80
w_low = -3
w_high = 3

