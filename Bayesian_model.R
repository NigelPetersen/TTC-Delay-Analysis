source(here("Github", "TTTC-Delay-Analysis", "EDA.R"))

100*(nrow(Delays_2023 |> filter(Min.Delay > 120))/nrow(Delays_2023))
Delays_2023 <- Delays_2023 |> filter(Min.Delay <= 120)

full_model <- glm(Min.Delay ~ ., data = Delays_2023, family = "poisson")
summary(full_model)

full_model <- step(full_model, trace = 0, direction = "backward")

full_fit <- full_model$fitted.values
full_res <- log((Delays_2023$Min.Delay - full_fit)^2)

# Check for overdispersion

halfnorm(residuals(full_model))

data.frame(residuals = full_res, fitted = full_fit) |>
  ggplot() +
  geom_point(aes(x = fitted, y = residuals)) +
  labs(x= "Fitted values", y = "Residuals", 
  title = "Residuals vs Fitted values") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_abline(slope = 1,yintercept = 0)

#adjust standard errors using overdispersion factor

disp_factor <- sum(residuals(full_model, type = "pearson")^2)/full_model$df.residual
summary(full_model, dispersion= disp_factor)



