# make sure to run "cues.R" before running this script
# this script can be run at the same time as "eut_fftrees.R"

# make sure you have the correct packages installed
# if not, run the following code:

#install.packages("tidyverse")
#install.packages("devtools")
#devtools::install_github("marcusbuckmann/ffcr")


library(ffcr)
library(tidyverse)

####ADDITIVE EE TREE####
fft_add <- fftree(
  data = sh_add_df,
  formula = choice ~ cue_min_g1 +cue_max_g1  + cue_increase, 
  method = "greedy",
  cv = TRUE,
  max_depth = 3 #can change to get different number of cues
)

print(fft_add)
plot(fft_add) 

####MULTIPLICATIVE EE TREE####
fft_mult <- fftree(
  data = sh_mult_df,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 3
)

plot(fft_mult)
print(fft_mult)
summary(fft_mult)

