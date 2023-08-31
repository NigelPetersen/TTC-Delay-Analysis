source(here("Github", "TTTC-Delay-Analysis", "EDA.R"))

Delays_2023 <- mutate_at(c("DayOfMonth", "Vehicle"), as.factor)

full_model <- glm(Min.Delay ~ ., data = Delays_2023, family = "poisson")
summary(full_model)

full_res <- full_model$residuals
full_fit <- full_model$fitted.values
full_pred <- log(full_fit)

# Check for overdispersion

data.frame(residuals = full_res, fitted = full_fit) |>
  ggplot() +
  geom_point(aes(x = fitted, y = log(residuals))) +
  labs(x= "Fitted values", y = "Residuals", 
  title = "Residuals vs Fitted values") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_hline(yintercept = 0)

