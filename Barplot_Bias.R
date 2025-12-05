library(tidyverse)
library(readxl)
all_articles <- read_excel("/Users/chrischen/Desktop/Fall 2025/COMP 370/Final Project/all_articles.xlsx")


order_of_bias <- c("Left","Center","Right")
order_of_stance <- c("Positive","Neutral","Negative")

country_and_polical_bias <- all_articles %>% 
  group_by(`Political Bias`,Country,`positive/neutral/negative`) %>% 
  summarise(count = n()) %>% 
  mutate(`Political Bias`=factor(`Political Bias`,levels = order_of_bias),
         `positive/neutral/negative`=factor(`positive/neutral/negative`,levels = order_of_stance),
         Sentiment = `positive/neutral/negative`) %>%
  ungroup(`positive/neutral/negative`) %>%
  mutate(Percentage = count/sum(count))

bias <- all_articles %>% 
  group_by(`Political Bias`,`positive/neutral/negative`) %>% 
  summarise(count = n()) %>% 
  mutate(`Political Bias`=factor(`Political Bias`,levels = order_of_bias),
         `positive/neutral/negative`=factor(`positive/neutral/negative`,levels = order_of_stance),
         Sentiment = `positive/neutral/negative`) %>%
  mutate(Percentage = count/sum(count))

g2 <- ggplot(bias,
             aes(x=`Political Bias`,
                 y=Percentage,
                 fill = Sentiment)) +
  geom_bar(stat = "identity",position = "dodge") +
  scale_fill_manual(values = c("Positive" = "green", "Neutral" = "grey","Negative" = "red")) + 
  ggtitle("Overall Distribution of Sentiment by Political Bias") +
  theme_linedraw(base_size = 25)


g3 <- ggplot(country_and_polical_bias,
             aes(x=`Political Bias`,
                 y=Percentage,
                 fill = Sentiment)) +
  geom_bar(stat = "identity",position = "dodge") +
  scale_fill_manual(values = c("Positive" = "green", "Neutral" = "grey","Negative" = "red")) + 
  facet_wrap(~`Country`) + 
  ggtitle("Comparative Sentiment Analysis by Political Bias") +
  theme_linedraw(base_size = 25)

combine_one_legend <- ggarrange(g2,g3,ncol =1,common.legend = TRUE,legend = "bottom")
combine_one_legend

ggsave("square_plot.png", plot = combine_one_legend, width = 11, height = 11, units = "in", dpi = 300)
