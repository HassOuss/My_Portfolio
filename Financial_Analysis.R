# Load libraries
library(shiny)
library(readr)
library(dplyr)
library(ggplot2)
library(skimr)
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
Balance_sheet_t_clean <- Balance_sheet_t %>%
  mutate(Year = as.Date(Year, format = "%m/%d/%Y"))

Cash_flow_t_clean <- Cash_flow_t %>%
  mutate(Year = as.Date(Year, format = "%m/%d/%Y"))

Income_t_clean <- Income_t %>%
  filter(Year != "ttm") %>% # remove ttm for plotting
  mutate(Year = as.Date(Year, format = "%m/%d/%Y"))

## Adding Quick Ratio to Balance Sheet column
Balance_sheet_t_clean <- Balance_sheet_t_clean %>%
  mutate(Quick_Ratio = (CurrentAssets - Inventory) / CurrentLiabilities)


########

ui <- fluidPage(
  titlePanel("Financial Analysis Dashboard"),
  
  # Balance Sheet Section
  h2("Balance Sheet Analysis"),
  h3("Quick Ratio"),
  plotOutput("quickRatioPlot"),
  
  h3("Assets vs Liabilities"),
  plotOutput("assetsLiabilitiesPlot"),
  
  tags$hr(),  # horizontal line for separation
  
  # Ratio Analysis Section
  h2("Ratio Analysis"),
  h3("Liquidity Ratios"),
  plotOutput("liquidityRatiosPlot"),
  
  h3("Profitability Ratios"),
  plotOutput("profitabilityRatiosPlot"),
  
  tags$hr(),
  
  # Cash Flow Section
  h2("Cash Flow Analysis"),
  h3("Operating, Investing & Financing"),
  plotOutput("cashFlowPlot"),
  
  tags$hr(),
  
  # Income Statement Section
  h2("Income Statement"),
  h3("Revenue, Gross Profit & EBITDA"),
  plotOutput("financialPlot")
)

#########
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
## Plot Operating Cash Flow vs Free Cash Flow
output$cashFlowPlot <- renderPlot({
ggplot(Cash_flow_t_clean, aes(x = Year)) +
  geom_line(aes(y = OperatingCashFlow, color = "Operating Cash Flow"), linewidth = 1.2) +
  geom_line(aes(y = FreeCashFlow, color = "Free Cash Flow"), linewidth = 1.2) +
  labs(
    title = "Operating Cash Flow vs Free Cash Flow",
    x = "Date",
    y = "Billions",
    color = "Metric"
  ) +
  theme_minimal()
 })
###Quick Ratio  
  output$quickRatioPlot <- renderPlot({
    ggplot(Balance_sheet_t_clean, aes(x = Year, y = Quick_Ratio)) +
      geom_line(color = "blue", size = 1) +        
      geom_point(color = "darkred", size = 2) +    
      geom_hline(yintercept = 1, linetype = "dashed", color = "black") + 
      geom_text(
        aes(label = round(Quick_Ratio, 2)),   
        vjust = -0.5, color = "black", size = 3.5
      ) +  
      labs(
        title = "Quick Ratio Over Time",
        x = "Year",
        y = "Quick Ratio"
      ) +
      theme_minimal()
  })
}

# Run the app
shinyApp(ui = ui, server = server)
