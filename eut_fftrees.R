# make sure to run "cues.R" before running this script
# this script can be run at the same time as "fftrees.R"

# make sure you have the correct packages installed
# if not, run the following code:

#install.packages("tidyverse")
#install.packages("devtools")
#devtools::install_github("marcusbuckmann/ffcr")

library(ffcr)
library(tidyverse)

####ADDITIVE TREES FOR VARYING ETA VALUES####
fft_add_0.25 <- fftree(
  data = sh_add_df_0.25,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 2
)

plot(fft_add_0.25)
print(fft_add_0.25)

###

fft_add_0.50 <- fftree(
  data = sh_add_df_0.50,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 3
)

plot(fft_add_0.50)
print(fft_add_0.50)

###

fft_add_0.75 <- fftree(
  data = sh_add_df_0.75,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 2
)

plot(fft_add_0.75)
print(fft_add_0.75)

###

fft_add_1.00 <- fftree(
  data = sh_add_df_1.00,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 3
)

plot(fft_add_1.00)
print(fft_add_1.00)

###

fft_add_1.50 <- fftree(
data = sh_add_df_1.50,
formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
method = "greedy",
cv = TRUE,
max_depth = 3
)

plot(fft_add_1.50)
print(fft_add_1.50)

####MULTIPLICATIVE TREES FOR VARYING ETA VALUES####

fft_mult_0.25 <- fftree(
  data = sh_mult_df_0.25,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 3
)

plot(fft_mult_0.25)
print(fft_mult_0.25)

###

fft_mult_0.50 <- fftree(
  data = sh_mult_df_0.50,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 3
)

plot(fft_mult_0.50)
print(fft_mult_0.50)

###

fft_mult_0.75 <- fftree(
  data = sh_mult_df_0.75,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 3
)

plot(fft_mult_0.75)
print(fft_mult_0.75)

###

fft_mult_1.00 <- fftree(
  data = sh_mult_df_1.00,
  formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
  method = "greedy",
  cv = TRUE,
  max_depth = 3
)

plot(fft_mult_1.00)
print(fft_mult_1.00)

###

fft_mult_1.50 <- fftree(
data = sh_mult_df_1.50,
formula = choice ~ cue_min_g1 +cue_max_g1 + cue_increase,
method = "greedy",
cv = TRUE,
max_depth = 3
)

plot(fft_mult_1.50)
print(fft_mult_1.50)
