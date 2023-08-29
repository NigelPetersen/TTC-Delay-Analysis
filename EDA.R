library(tidyverse)
library(rstan)
library(tidybayes)
library(ggplot2)
library(here)
library(bayesplot)
library(loo)
library(readr)

get_time <- function(mins){
  num_hours = floor(mins/60)
  num_mins = mins - 60*num_hours
  return(c(num_hours, num_mins))
}

Delays_2023 = read.csv(here("Github", "TTTC-Delay-Analysis", 
               "cleaned_delays_2023.csv"))

Delays_2023 |> filter(Min.Delay >0 & Min.Delay <=100) |>
  ggplot() + geom_point(aes(x=Time, y=Min.Delay)) +
  labs(x = "Time (minutes)", y = "Delay time (minutes)")


Delays_2023 |> mutate(time_block = floor(Time/60)) |>
  group_by(time_block, Line) |>
  summarize(delay_by_time = mean(Min.Delay)) |>
  ggplot(aes(x = time_block, y = delay_by_time, color = Line)) + 
  geom_line() +
  labs(x = "One hour time intervals (24 hour time)",
       y = "Average delay time (minutes)",
       title = "Delay times per hour interval") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5))
