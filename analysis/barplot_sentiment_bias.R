library(tidyverse)
library(scales)
library(readxl)
library(ggpubr)

path <- file.path(getwd(), '..', 'data', 'all_articles.xlsx')
all_articles <- read_excel(path)

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
  geom_text(aes(label = paste0(round(100*Percentage, 1), "%")),
            stat = "identity",
            position = position_dodge(width = 0.9),
            size = 6,
            vjust = -0.7) +
  scale_y_continuous(labels = scales::percent,expand = expansion(mult = c(0, 0.15))) +
  scale_fill_manual(values = c("Positive" = "green3", "Neutral" = "grey","Negative" = "red3")) + 
  ggtitle("Overall Distribution of Sentiment by Political Bias") +
  theme_linedraw(base_size = 25)


g3 <- ggplot(country_and_polical_bias,
             aes(x=`Political Bias`,
                 y=Percentage,
                 fill = Sentiment)) +
  geom_bar(stat = "identity",position = "dodge") +
  geom_text(aes(label = paste0(round(100*Percentage, 1), "%")),
            stat = "identity",
            position = position_dodge(width = 0.9),
            size = 4,
            vjust = -0.7) +
  scale_y_continuous(labels = scales::percent,expand = expansion(mult = c(0, 0.15))) +
  scale_fill_manual(values = c("Positive" = "green3", "Neutral" = "grey","Negative" = "red3")) + 
  facet_wrap(~`Country`) + 
  ggtitle("Comparative Sentiment Analysis by Political Bias") +
  theme_linedraw(base_size = 25)

combine_one_legend <- ggarrange(g2,g3,ncol =1,common.legend = TRUE,legend = "bottom")
combine_one_legend

ggsave("square_plot.png", plot = combine_one_legend, width = 11, height = 11, units = "in", dpi = 300)

