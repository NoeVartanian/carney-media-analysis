library(tidyverse)
library(readxl)

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

input_file <- "all_articles_full.xlsx"     
topic_col <- "open coding/categories"
country_col <- "Country"

country_of_interest <- "Canada"            


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df <- read_excel("/Users/noevartanian/Documents/COMP/Project370/Analysis/all_articles_full.xlsx")

# ------------------------------------------------------------
# FILTER DATA
# ------------------------------------------------------------

df_filtered <- df %>%
  filter(
    !is.na(.data[[topic_col]]),
    !is.na(.data[[country_col]]),
    .data[[country_col]] == country_of_interest
  )

if (nrow(df_filtered) == 0) {
  stop(paste("No rows found for country:", country_of_interest))
}

# ------------------------------------------------------------
# COMPUTE PERCENTAGE OF EACH TOPIC
# ------------------------------------------------------------

topic_pct <- df_filtered %>%
  count(topic = .data[[topic_col]]) %>%
  mutate(
    pct = n / sum(n) * 100,
    topic_label = dplyr::case_when(
      topic == "2025 Elections/Campaigning/Federal Parties" ~ "2025 Election and Federal Parties",
      topic == "Biography/Opinion/Criticism/Personal Details" ~ "Biography and Opinion",
      topic == "Canada/US Relations" ~ "Canada and US Relations",
      topic == "Canadian Domestic Governance/Economy/Industry" ~ "Canadian Governance and Economy",
      topic == "Culture/Social life/Events/Sports" ~ "Culture and Social Life",
      topic == "International Relations & Diplomacy" ~ "International Relations and Diplomacy",
      TRUE ~ topic
    )
  )

# ------------------------------------------------------------
# PIE CHART (with % labels pushed outward)
# ------------------------------------------------------------

ggplot(topic_pct, aes(x = "", y = pct, fill = topic_label)) +
  geom_col(width = 2, color = "black") +
  coord_polar(theta = "y") +
  geom_text(
    aes(
      x = 1.75,                                
      label = paste0(round(pct, 1), "%")
    ),
    position = position_stack(vjust = 0.5),
    size = 5
  ) +
  labs(
    title = paste("Distribution of Topics Within", country_of_interest),
    fill = "Topic"
  ) +
  theme_void() +
  theme(
    plot.title   = element_text(hjust = 0.5, size = 20),
    legend.title = element_text(size = 15),
    legend.text  = element_text(size = 13)
  )

