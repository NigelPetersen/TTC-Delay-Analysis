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

Delays_2023 |> mutate(Line = recode(Line,
  "YU" = "Yonge-University", "SHP" = "Sheppard",
  "SRT" = "Scarborough", "BD" = "Bloor-Danforth")) |>
  mutate(time_block = floor(Time/60)) |>
  group_by(time_block, Line) |>
  summarize(delay_by_time = mean(Min.Delay)) |>
  ggplot(aes(x = time_block, y = delay_by_time, color = Line)) + 
  geom_line(linewidth = 0.7) +
  labs(x = "One hour time intervals (24 hour time)",
       y = "Average delay time (minutes)",
       title = "Delay times per hour interval") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5)) + 
  annotate("rect", xmin = 6, xmax = 10, ymin = -Inf, 
           ymax = Inf, alpha = 0.1, fill = "blue") +
  annotate("rect", xmin = 15, xmax = 19, ymin = -Inf,
           ymax = Inf, alpha = 0.1, fill = "red")


Delays_2023 |> mutate(Line = recode(Line,
  "YU" = "Yonge-University", "SHP" = "Sheppard",
  "SRT" = "Scarborough", "BD" = "Bloor-Danforth")) |> 
  ggplot() + 
  geom_bar(aes(x = Line), fill= "blue", alpha = 0.2) +
  labs(x = "Transit Line", y = "Count", 
       title = "Frequency of transit lines") +
  theme_bw() +
  theme(plot.title = element_text(hjust=0.5)) +
  scale_fill_discrete(labels = c("Bloor-Danforth",
  "Sheppard", "Scarborough", "Yonge-University"))
  