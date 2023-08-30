source(here("Github", "TTTC-Delay-Analysis", "EDA.R"))

poisson_model = glm(Min.Delay ~ ., data = Delays_2023, family = "poisson")
summary(poisson_model)
