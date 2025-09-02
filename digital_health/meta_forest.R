library(metafor)

data <- read.csv("/Users/wangmengting/Desktop/SatisfactionScore.csv")

res <- rma(
  yi = data$SMD,
  sei = sqrt(data$Variance),
  method = "DL",
  data = data
)

weights <- weights(res)
weights_pct <- round(weights / sum(weights) * 100, 1)

labels <- paste0(data$Study, ", ", data$Outcome)

ci_text <- paste0(
  sprintf("%.2f", data$SMD), 
  " [", 
  sprintf("%.2f", res$ci.lb), 
  ", ", 
  sprintf("%.2f", res$ci.ub), 
  "]"
)

table_text <- cbind(
  Study = data$Study,
  Tool = data$Outcome,
  `Hedges' g` = sprintf("%.2f", data$SMD),
  `SMD [95%% CI]` = ci_text,
  `Weight %%` = paste0(weights_pct, "%")
)

forest(
  res,
  xlim = c(-2, 2),
  at = c(-1.5, -1, -0.5, 0, 0.5, 1, 1.5),
  ilab = table_text[, -1],  
  ilab.xpos = c(-1.1, -0.5, 0.5, 1.3), 
  slab = table_text[, 1], 
  mlab = paste0("Random-Effects Model (I² = ", round(res$I2, 1), "%, ",
                "τ² = ", round(res$tau2, 2), ", p = ", formatC(res$QEp, format="f", digits=2), ")"),
  xlab = "Standardised Mean Difference"
)

text(
  -2, 
  length(data$SMD) + 1, 
  pos = 4,
  labels = "Study"
)
text(-1.1, length(data$SMD) + 1, "Outcome")
text(-0.5, length(data$SMD) + 1, "Hedges' g")
text(0.5, length(data$SMD) + 1, "SMD [95% CI]")
text(1.3, length(data$SMD) + 1, "Weight%")
