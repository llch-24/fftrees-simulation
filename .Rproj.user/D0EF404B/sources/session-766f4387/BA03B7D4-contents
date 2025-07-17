# this is the first script to run, which will
# clean all csv files and engineer binary cues

# make sure you have the correct packages installed
# if not, run the following code:

#install.packages("tidyverse")
#install.packages("devtools")
#devtools::install_github("marcusbuckmann/ffcr")

library(ffcr)
library(tidyverse)

#the following code loads and cleans all relevant csv files
####CSV FILES####
add_df <- read_csv("ee_additive_dataset.csv")
mult_df <- read_csv("ee_multiplicative_dataset.csv")

add_0.25 <- read_csv("additive_sim_eta_0.25.csv")
add_0.5 <- read_csv("additive_sim_eta_0.50.csv")
add_0.75 <- read_csv("additive_sim_eta_0.75.csv")
add_1.00 <- read_csv("additive_sim_eta_1.00.csv")
add_1.50 <- read_csv("additive_sim_eta_1.50.csv")

mult_0.25 <- read_csv("multiplicative_sim_eta_0.25.csv")
mult_0.5 <- read_csv("multiplicative_sim_eta_0.50.csv")
mult_0.75 <- read_csv("multiplicative_sim_eta_0.75.csv")
mult_1.00 <- read_csv("multiplicative_sim_eta_1.00.csv")
mult_1.50 <- read_csv("multiplicative_sim_eta_1.50.csv")

####CLEAN CSV FILES####
sh_add_df <- add_df |>
  mutate(choice = factor(
    if_else(ee_choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ))  |>
  mutate(
    cue_max_g1 = g1_max > g2_max,
    cue_min_g1 = g1_min > g2_min,
    cue_pos_g1 = g1_count_positive > g2_count_positive,
    cue_smaller_range_g1 = g1_range < g2_range,
    cue_min_above_zero_g1 = g1_min > 0 & g2_min < 0,
    cue_any_pos_vs_none = g1_count_positive > 0 & g2_count_positive == 0,
  ) |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_a,
         -g1_b,
         -g2_a,
         -g2_b,
         -g1_mean,
         -g2_mean,
         -g1_both_shrinkers,
         -g2_both_gainers,
         -g2_both_shrinkers,
         -g1_both_gainers,
         -g2_both_shrinkers,
         -g1_count_gainers,
         -g1_count_shrinkers,
         -g2_count_shrinkers,
         -g2_count_gainers)

has_pos <- "cue_pos_g1" %in% names(sh_add_df)
has_gainers <- "cue_more_gainers" %in% names(sh_add_df)

sh_add_df <- sh_add_df |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )


sh_mult_df <- mult_df |>
  mutate(choice = factor(
    if_else(ee_choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ),
  cue_max_g1 = g1_max > g2_max,
  cue_min_g1 = g1_min > g2_min,
  cue_smaller_range_g1 = g1_range < g2_range,
  cue_more_gainers = g1_count_gainers > g2_count_gainers
  )  |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_a,
         -g1_b,
         -g2_a,
         -g2_b,
         -g1_signs_diff,
         -g2_signs_diff,
         -g1_mean,
         -g2_mean,
         -g1_both_positive,
         -g1_both_negative,
         -g2_both_positive,
         -g2_both_negative,
         -g1_count_negative,
         -g1_count_positive,
         -g2_count_negative,
         -g2_count_positive)

has_pos <- "cue_pos_g1" %in% names(sh_mult_df)
has_gainers <- "cue_more_gainers" %in% names(sh_mult_df)

sh_mult_df <- sh_mult_df |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )


# additive eut functions
sh_add_df_0.25 <- add_0.25 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ))  |>
  mutate(
    cue_max_g1 = g1_max > g2_max,
    cue_min_g1 = g1_min > g2_min,
    cue_pos_g1 = g1_count_positive > g2_count_positive,
    cue_smaller_range_g1 = g1_range < g2_range,
    cue_min_above_zero_g1 = g1_min > 0 & g2_min < 0,
    cue_any_pos_vs_none = g1_count_positive > 0 & g2_count_positive == 0
  ) |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_mean,
         -g2_mean,
         -g2_both_gainers,
         -g2_both_shrinkers,
         -g1_both_gainers,
         -g2_both_shrinkers,
         -g1_count_gainers,
         -g1_count_shrinkers,
         -g2_count_shrinkers,
         -g2_count_gainers)

has_pos <- "cue_pos_g1" %in% names(sh_add_df_0.25)
has_gainers <- "cue_more_gainers" %in% names(sh_add_df_0.25)

sh_add_df_0.25 <- sh_add_df_0.25 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )

sh_add_df_0.50 <- add_0.5 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ))  |>
  mutate(
    cue_max_g1 = g1_max > g2_max,
    cue_min_g1 = g1_min > g2_min,
    cue_pos_g1 = g1_count_positive > g2_count_positive,
    cue_smaller_range_g1 = g1_range < g2_range,
    cue_min_above_zero_g1 = g1_min > 0 & g2_min < 0,
    cue_any_pos_vs_none = g1_count_positive > 0 & g2_count_positive == 0
  ) |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_mean,
         -g2_mean,
         -g2_both_gainers,
         -g2_both_shrinkers,
         -g1_both_gainers,
         -g2_both_shrinkers,
         -g1_count_gainers,
         -g1_count_shrinkers,
         -g2_count_shrinkers,
         -g2_count_gainers)

has_pos <- "cue_pos_g1" %in% names(sh_add_df_0.50)
has_gainers <- "cue_more_gainers" %in% names(sh_add_df_0.50)

sh_add_df_0.50 <- sh_add_df_0.50 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )

sh_add_df_0.75 <- add_0.75 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ))  |>
  mutate(
    cue_max_g1 = g1_max > g2_max,
    cue_min_g1 = g1_min > g2_min,
    cue_pos_g1 = g1_count_positive > g2_count_positive,
    cue_smaller_range_g1 = g1_range < g2_range,
    cue_min_above_zero_g1 = g1_min > 0 & g2_min < 0,
    cue_any_pos_vs_none = g1_count_positive > 0 & g2_count_positive == 0
  ) |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_mean,
         -g2_mean,
         -g2_both_gainers,
         -g2_both_shrinkers,
         -g1_both_gainers,
         -g2_both_shrinkers,
         -g1_count_gainers,
         -g1_count_shrinkers,
         -g2_count_shrinkers,
         -g2_count_gainers)

has_pos <- "cue_pos_g1" %in% names(sh_add_df_0.75)
has_gainers <- "cue_more_gainers" %in% names(sh_add_df_0.75)

sh_add_df_0.75 <- sh_add_df_0.75 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )

sh_add_df_1.00 <- add_1.00 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ))  |>
  mutate(
    cue_max_g1 = g1_max > g2_max,
    cue_min_g1 = g1_min > g2_min,
    cue_pos_g1 = g1_count_positive > g2_count_positive,
    cue_smaller_range_g1 = g1_range < g2_range,
    cue_min_above_zero_g1 = g1_min > 0 & g2_min < 0,
    cue_any_pos_vs_none = g1_count_positive > 0 & g2_count_positive == 0
  ) |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_mean,
         -g2_mean,
         -g2_both_gainers,
         -g2_both_shrinkers,
         -g1_both_gainers,
         -g2_both_shrinkers,
         -g1_count_gainers,
         -g1_count_shrinkers,
         -g2_count_shrinkers,
         -g2_count_gainers)

has_pos <- "cue_pos_g1" %in% names(sh_add_df_1.00)
has_gainers <- "cue_more_gainers" %in% names(sh_add_df_1.00)

sh_add_df_1.00 <- sh_add_df_1.00 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )

sh_add_df_1.50 <- add_1.50 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ))  |>
  mutate(
    cue_max_g1 = g1_max > g2_max,
    cue_min_g1 = g1_min > g2_min,
    cue_pos_g1 = g1_count_positive > g2_count_positive,
    cue_smaller_range_g1 = g1_range < g2_range,
    cue_min_above_zero_g1 = g1_min > 0 & g2_min < 0,
    cue_any_pos_vs_none = g1_count_positive > 0 & g2_count_positive == 0
  ) |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_mean,
         -g2_mean,
         -g2_both_gainers,
         -g2_both_shrinkers,
         -g1_both_gainers,
         -g2_both_shrinkers,
         -g1_count_gainers,
         -g1_count_shrinkers,
         -g2_count_shrinkers,
         -g2_count_gainers)

has_pos <- "cue_pos_g1" %in% names(sh_add_df_1.50)
has_gainers <- "cue_more_gainers" %in% names(sh_add_df_1.50)
sh_add_df_1.50 <- sh_add_df_1.50 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )


# multiplicative eut

sh_mult_df_0.25 <- mult_0.25 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ),
  cue_max_g1 = g1_max > g2_max,
  cue_min_g1 = g1_min > g2_min,
  cue_smaller_range_g1 = g1_range < g2_range,
  cue_more_gainers = g1_count_gainers > g2_count_gainers
  )  |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_signs_diff,
         -g2_signs_diff,
         -g1_mean,
         -g2_mean,
         -g1_both_positive,
         -g1_both_negative,
         -g2_both_positive,
         -g2_both_negative,
         -g1_count_negative,
         -g1_count_positive,
         -g2_count_negative,
         -g2_count_positive)

has_pos <- "cue_pos_g1" %in% names(sh_mult_df_0.25)
has_gainers <- "cue_more_gainers" %in% names(sh_mult_df_0.25)
sh_mult_df_0.25 <- sh_mult_df_0.25 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )




sh_mult_df_0.50 <- mult_0.5 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ),
  cue_max_g1 = g1_max > g2_max,
  cue_min_g1 = g1_min > g2_min,
  cue_smaller_range_g1 = g1_range < g2_range,
  cue_more_gainers = g1_count_gainers > g2_count_gainers
  )  |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_signs_diff,
         -g2_signs_diff,
         -g1_mean,
         -g2_mean,
         -g1_both_positive,
         -g1_both_negative,
         -g2_both_positive,
         -g2_both_negative,
         -g1_count_negative,
         -g1_count_positive,
         -g2_count_negative,
         -g2_count_positive)

has_pos <- "cue_pos_g1" %in% names(sh_mult_df_0.50)
has_gainers <- "cue_more_gainers" %in% names(sh_mult_df_0.50)
sh_mult_df_0.50 <- sh_mult_df_0.50 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )

sh_mult_df_0.75 <- mult_0.75 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ),
  cue_max_g1 = g1_max > g2_max,
  cue_min_g1 = g1_min > g2_min,
  cue_smaller_range_g1 = g1_range < g2_range,
  cue_more_gainers = g1_count_gainers > g2_count_gainers
  )  |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_signs_diff,
         -g2_signs_diff,
         -g1_mean,
         -g2_mean,
         -g1_both_positive,
         -g1_both_negative,
         -g2_both_positive,
         -g2_both_negative,
         -g1_count_negative,
         -g1_count_positive,
         -g2_count_negative,
         -g2_count_positive)

has_pos <- "cue_pos_g1" %in% names(sh_mult_df_0.75)
has_gainers <- "cue_more_gainers" %in% names(sh_mult_df_0.75)
sh_mult_df_0.75 <- sh_mult_df_0.75 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )



sh_mult_df_1.00 <- mult_1.00 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ),
  cue_max_g1 = g1_max > g2_max,
  cue_min_g1 = g1_min > g2_min,
  cue_smaller_range_g1 = g1_range < g2_range,
  cue_more_gainers = g1_count_gainers > g2_count_gainers
  )  |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_signs_diff,
         -g2_signs_diff,
         -g1_mean,
         -g2_mean,
         -g1_both_positive,
         -g1_both_negative,
         -g2_both_positive,
         -g2_both_negative,
         -g1_count_negative,
         -g1_count_positive,
         -g2_count_negative,
         -g2_count_positive)

has_pos <- "cue_pos_g1" %in% names(sh_mult_df_1.00)
has_gainers <- "cue_more_gainers" %in% names(sh_mult_df_1.00)
sh_mult_df_1.00 <- sh_mult_df_1.00 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )


sh_mult_df_1.50 <- mult_1.50 |>
  mutate(choice = factor(
    if_else(choice == 1, "g1", "g2"),
    levels = c("g2", "g1") # g2 = F, g1 = T
  ),
  cue_max_g1 = g1_max > g2_max,
  cue_min_g1 = g1_min > g2_min,
  cue_smaller_range_g1 = g1_range < g2_range,
  cue_more_gainers = g1_count_gainers > g2_count_gainers
  )  |>
  select(choice,
         starts_with("cue_"),
         starts_with("g1_"),
         starts_with("g2_"),
         -g1_signs_diff,
         -g2_signs_diff,
         -g1_mean,
         -g2_mean,
         -g1_both_positive,
         -g1_both_negative,
         -g2_both_positive,
         -g2_both_negative,
         -g1_count_negative,
         -g1_count_positive,
         -g2_count_negative,
         -g2_count_positive)

has_pos <- "cue_pos_g1" %in% names(sh_mult_df_1.50)
has_gainers <- "cue_more_gainers" %in% names(sh_mult_df_1.50)
sh_mult_df_1.50 <- sh_mult_df_1.50 |>
  mutate(
    cue_increase =
      (if (has_pos) coalesce(cue_pos_g1, FALSE) else FALSE) |
      (if (has_gainers) coalesce(cue_more_gainers, FALSE) else FALSE)
  )
