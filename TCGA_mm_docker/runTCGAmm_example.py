from TCGA_matchmaker import match_computation as m
import pandas as pd 

profile = pd.Series([2,3,4], index = ["g1","g2","g3"])
print("The ref profile is:")
print(profile)

sample_data = pd.Series([2,4,4,5], index = ["g1","g2","g4","g5"])
print("The sample profile is:")
print(sample_data)

distance = m.compute_distance(profile, sample_data)
print("The diastance is:")
print(distance)
