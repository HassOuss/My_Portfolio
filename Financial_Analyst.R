# Load libraries
library(shiny)
library(readr)
library(dplyr)
library(ggplot2)
library(skimr)
library(readr)
library(tidyr)
library(reshape2)

# Load data in Shiny
balance_sheet <- read_csv("https://raw.githubusercontent.com/HassOuss/My_Portfolio/refs/heads/main/Balance_sheet.csv")
cash_flow <- read_csv("https://raw.githubusercontent.com/HassOuss/My_Portfolio/refs/heads/main/Cash_flow.csv")
income <- read_csv("https://raw.githubusercontent.com/HassOuss/My_Portfolio/refs/heads/main/Financials.csv")  


# Transpose variables because they are in rows
Balance_sheet_t <- balance_sheet %>%
  pivot_longer(cols = -1, names_to = "Year", values_to = "Value") %>%
  pivot_wider(names_from = 1, values_from = Value)

Cash_flow_t <- cash_flow %>%
  pivot_longer(cols = -1, names_to = "Year", values_to = "Value") %>%
  pivot_wider(names_from = 1, values_from = Value)

Income_t <- income %>%
  pivot_longer(cols = -1, names_to = "Year", values_to = "Value") %>%
  pivot_wider(names_from = 1, values_from = Value)


# Prepare cleaned data
Income_t_clean <- Income_t %>%
  filter(Year != "ttm") %>% # remove ttm for plotting
  mutate(Year = as.Date(Year, format = "%m/%d/%Y"))

# Define UI
ui <- fluidPage(
  titlePanel("Financial Performance Over Time"),
  sidebarLayout(
    sidebarPanel(
      helpText("This app displays Total Revenue, Gross Profit, and EBITDA over time.")
    ),
    mainPanel(
      plotOutput("financialPlot") ) ))

# Define Server
server <- function(input, output) {
  output$financialPlot <- renderPlot({
    ggplot(Income_t_clean, aes(x = Year)) +
      geom_line(aes(y = TotalRevenue, color = "Total Revenue"), linewidth = 1) +
      geom_line(aes(y = GrossProfit, color = "Gross Profit"), linewidth = 1) +
      geom_line(aes(y = EBITDA, color = "EBITDA"), linewidth = 1) +
      labs(
        title = "Total Revenue, Gross Profit, and EBITDA Over Time",
        y = "Value (Billions)",
        x = "Date",
        color = "Metric"
      ) +
      theme_minimal()
  })
}

# Run the app
shinyApp(ui = ui, server = server)
