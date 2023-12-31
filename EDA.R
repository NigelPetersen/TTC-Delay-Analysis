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

Delays_2023 <- Delays_2023 |> select(-X)

get_avg_by <- function(data, col){
  data |> group_by(data[col]) |>
    summarize(mean_delay = mean(Min.Delay), mean_gap = mean(Min.Gap)) |>
    mutate(average_delay = mean(Delays_2023$Min.Delay),
           average_gap = mean(Delays_2023$Min.Gap))
}


bound <- Delays_2023 |> mutate(Bound = recode(Bound, "N" = "North",
        "E" = "East", "W" = "West", "S" = "South"))
line <- Delays_2023 |> mutate(Line = recode(Line, "YU" = "Yonge-University",
        "SHP" = "Sheppard", "SRT" = "Scarborough", "BD" = "Bloor-Danforth")) 

get_avg_by(bound, "Bound")
get_avg_by(line, "Line")
get_avg_by(Delays_2023, "Day")
get_avg_by(Delays_2023, "Month")
get_avg_by(Delays_2023, "Station")


line |>
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



line |> 
  ggplot() + 
  geom_bar(aes(x = Line), fill= "blue", alpha = 0.2) +
  labs(x = "Transit Line", y = "Count", 
       title = "Frequency of transit lines") +
  theme_bw() +
  theme(plot.title = element_text(hjust=0.5)) +
  scale_fill_discrete(labels = c("Bloor-Danforth",
  "Sheppard", "Scarborough", "Yonge-University"))



line |>
  mutate(time_block = floor(Time/60)) |>
  group_by(time_block, Line) |>
  summarize(gap_by_time = mean(Min.Gap)) |>
  ggplot(aes(x = time_block, y = gap_by_time, color = Line)) + 
  geom_line(linewidth = 0.7) +
  labs(x = "One hour time intervals (24 hour time)",
       y = "Average delay time to next train (minutes)",
       title = "Delay times between trains per hour interval") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5)) + 
  annotate("rect", xmin = 6, xmax = 10, ymin = -Inf, 
           ymax = Inf, alpha = 0.1, fill = "blue") +
  annotate("rect", xmin = 15, xmax = 19, ymin = -Inf,
           ymax = Inf, alpha = 0.1, fill = "red")


Delays_2023 |> group_by(Station) |>
  ggplot() + 
  geom_bar(aes(x = Station), fill = "blue", alpha = 0.2) +
  theme_bw() +
  labs(x = "Station", y = "Count", 
       title = "Frequency of rides across stations") +
  theme(axis.text.x = element_text(angle = 270), 
        plot.title = element_text(hjust = 0.5))


Delays_2023 |> filter(Min.Delay < 200) |>
  group_by(Station) |> 
  ggplot() + 
  geom_boxplot(aes(x = reorder(Station,Min.Delay), y = Min.Delay)) +
  theme_bw() + theme(axis.text.x = element_text(angle = 270)) +
  labs(x = "Station", y = "Delay (minutes)", 
       title = "Average delay by station") +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_hline(yintercept = mean(Delays_2023$Min.Delay), color = "red")


days_of_the_week <- unique(Delays_2023$Day)

line |>
  filter(Min.Delay < 200) |>
  group_by(Day, Line) |>
  ggplot() + 
  geom_boxplot(aes(x = factor(Day, days_of_the_week), y = Min.Delay, 
  color = Line)) + theme_bw() + 
  labs(x = "Day of the week", y = "Delay (minutes)", 
       title = "Delay times across transit lines throughout the week") + 
  theme(plot.title = element_text(hjust = 0.5))







