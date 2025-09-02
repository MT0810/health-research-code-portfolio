library(metafor)
library(ggplot2)

data <- read.csv("/Users/wangmengting/Desktop/SatisfactionScore.csv")
data$SE <- sqrt(data$Variance)

res <- rma(yi = data$SMD, sei = data$SE, method = "DL")

loo_df <- as.data.frame(leave1out(res))

plot_df <- data.frame(
  Study    = data$Study,
  Outcome  = data$Outcome,
  Estimate = round(loo_df$estimate, 3),
  CI.lb    = round(loo_df$ci.lb, 3),
  CI.ub    = round(loo_df$ci.ub, 3)
)

# Label
plot_df$Label <- paste0(plot_df$Study, "\n", plot_df$Outcome)
plot_df$Label <- factor(plot_df$Label, levels = rev(plot_df$Label))  # 保持原始顺序（从上到下）

plot_df$Text_Label <- paste0("CI: [", plot_df$CI.lb, ", ", plot_df$CI.ub, "]\nEst: ", plot_df$Estimate)

p <- ggplot(plot_df, aes(x = Estimate, y = Label)) +
  geom_point(color = "blue", size = 2) +
  geom_errorbarh(aes(xmin = CI.lb, xmax = CI.ub), height = 0.2) +
  geom_vline(xintercept = res$b, linetype = "dashed", color = "red") +
  geom_text(aes(label = Text_Label), hjust = -0.1, size = 3.1) +
  labs(
    x = "Effect Size (SMD)",
    y = NULL,
    title = "Leave-One-Out Sensitivity Analysis"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    axis.text.y = element_text(hjust = 1, size = 10),
    plot.title = element_text(face = "bold", hjust = 0.5)
  ) +
  xlim(min(plot_df$CI.lb) - 0.05, max(plot_df$CI.ub) + 0.25) 
