# Load libraries
library(shiny)
library(readr)
library(dplyr)
library(ggplot2)
library(skimr)
library(tidyr)
library(reshape2)
library(scales)

# Load data in Shiny
balance_sheet <- read_csv("https://raw.githubusercontent.com/HassOuss/My_Portfolio/refs/heads/main/Balance_sheet.csv")
cash_flow <- read_csv("https://raw.githubusercontent.com/HassOuss/My_Portfolio/refs/heads/main/Cash_flow.csv")
income <- read_csv("https://raw.githubusercontent.com/HassOuss/My_Portfolio/refs/heads/main/Financials.csv")  


# Transpose variables because they are in rows
Balance_sheet_t <- balance_sheet %>%
  pivot_longer(cols = -1, names_to = "Year", values_to = "Value") %>%
  pivot_wider(names_from = 1, values_from = Value)

Cash_flow_t <- cash_flow %>%
  pivot_longer(cols = -1, names_to = "Observation", values_to = "Value") %>%
  pivot_wider(names_from = 1, values_from = Value)

Income_t <- income %>%
  pivot_longer(cols = -1, names_to = "Observation", values_to = "Value") %>%
  pivot_wider(names_from = 1, values_from = Value)


# Prepare cleaned data
Balance_sheet_t_clean <- Balance_sheet_t %>%
  mutate(Year = as.Date(Year, format = "%m/%d/%Y"))

Cash_flow_t_clean <- Cash_flow_t %>%
  filter(Observation != "ttm") %>% # remove ttm for plotting
  mutate(Observation = as.Date(Observation, format = "%m/%d/%Y"))

Income_t_clean <- Income_t %>%
  filter(Observation != "ttm") %>% # remove ttm for plotting
  mutate(Observation = as.Date(Observation, format = "%m/%d/%Y"))

## Adding Quick Ratio to Balance Sheet column
Balance_sheet_t_clean <- Balance_sheet_t_clean %>%
  mutate(Quick_Ratio = (CurrentAssets - Inventory) / CurrentLiabilities)
## Adding Profit Margin to Income Sheet
#Income_t_clean$ProfitMargin <- (Income_t_clean$NetIncome / Income_t_clean$TotalRevenue) * 100

# ==== Data prep (outside server) ====
Balance_sheet_t_clean <- Balance_sheet_t_clean %>%
  mutate(CurrentRatio = CurrentAssets / CurrentLiabilities)

Income_t_clean <- Income_t %>%
  filter(Observation != "ttm") %>%
  mutate(
    Observation = as.Date(Observation, format = "%m/%d/%Y"),
    ProfitMargin = (NetIncome / TotalRevenue) * 100
  )

Income_t_factor <- Income_t_clean %>%
  mutate(Observation = factor(format(Observation, "%Y-%m")))

income_long <- Income_t_factor %>%
  select(Observation, TotalRevenue, NetIncome, ProfitMargin) %>%
  pivot_longer(cols = c(TotalRevenue, NetIncome),
               names_to = "Metric", values_to = "Value")

scale_factor <- max(c(max(Income_t_clean$TotalRevenue, na.rm = TRUE),
                      max(Income_t_clean$NetIncome, na.rm = TRUE)))


########

ui <- fluidPage(
  titlePanel("Financial Analysis Dashboard"),

   # Ratio Analysis Section
  h2("Ratio Analysis"),
  h3("Quick Ratio"),
  plotOutput("quickRatioPlot"),
  
  h3("Current Ratio"),
  plotOutput("currentRatioPlot"),
  
  h3("Liquidity Ratios"),
  plotOutput("liquidityRatiosPlot"),
  
  h3("Profitability Ratios"),
  plotOutput("profitabilityRatiosPlot"),
  tags$hr(),
  
  # Balance Sheet Section
  h2("Balance Sheet Analysis"),
  #h3("Quick Ratio"),
  #plotOutput("quickRatioPlot"),
  
  h3("Assets vs Liabilities"),
  plotOutput("assetsLiabilitiesPlot"),
  
  tags$hr(),  # horizontal line for separation
  
  # Cash Flow Section
  h2("Cash Flow Analysis"),
  h3("Operating, Investing & Financing"),
  plotOutput("cashFlowPlot"),
  
  tags$hr(),
  
  # Income Statement Section
  h2("Income Statement"),
  h3("Revenue, Gross Profit & EBITDA"),
  plotOutput("financialPlot"),
  plotOutput("EBITDA_NetIncPlot"),
  plotOutput("TRev_TExPlot"),
  plotOutput("revNetIncomePlot")
)

#########
# Define Server
server <- function(input, output) {
  output$currentRatioPlot <- renderPlot({
  ggplot(Balance_sheet_t_clean, aes(x = Observation)) +
    # Bars for Assets and Liabilities
    geom_col(aes(y = `CurrentAssets`, fill = "CurrentAssets"), position = "dodge", width = 0.4) +
    geom_col(aes(y = `CurrentLiabilities`, fill = "CurrentLiabilities"), position = "dodge", width = 0.4) +
    
    # Line for Current Ratio (secondary axis)
    geom_line(aes(y = CurrentRatio, group = 1, color = "CurrentRatio"), size = 1.2) +
    geom_point(aes(y = CurrentRatio, color = "CurrentRatio"), size = 2) +
    
    scale_y_continuous(
      name = "Assets & Liabilities (Billions)",
      sec.axis = sec_axis(~./100, name = "Current Ratio")
    ) +
    
    scale_fill_manual(values = c("CurrentAssets" = "steelblue", "CurrentLiabilities" = "tomato")) +
    scale_color_manual(values = c("CurrentRatio" = "darkgreen")) +
    
    labs(
      title = "Current Assets, Liabilities, and Current Ratio",
      x = "Date", fill = "", color = ""
    ) + theme_minimal()
})

  
  ###
  output$financialPlot <- renderPlot({
    ggplot(Income_t_clean, aes(x = Observation)) +
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
## Plot EBITDA & Net Income
# show company's financial performance

  output$EBITDA_NetIncPlot <- renderPlot({
  ggplot(Income_t_clean, aes(x = Observation)) +
  geom_line(aes(y = EBITDA, color = "EBITDA"), linewidth = 1) +
  geom_line(aes(y = NetIncome, color = "Net Income"), linewidth = 1) +
  labs(
    title = "EBITDA & Net Income Over Time",
    x = "Date",
    y = "Billions",
    color = "Metric"
  ) +
  theme_minimal()
    }) 

## Hybrid: Operating Cash Flow (bars) + Free Cash Flow (line)
Cash_flow_t_clean$Observation <- as.factor(Cash_flow_t_clean$Observation)
output$cashFlowPlot <- renderPlot({
  ggplot(Cash_flow_t_clean, aes(x = Observation)) +
    # Bars for Operating Cash Flow
    geom_col(aes(y = OperatingCashFlow, fill = "Operating Cash Flow"), width = 0.6, alpha = 0.8) +
    
    # Line for Free Cash Flow
    geom_line(aes(y = FreeCashFlow, color = "Free Cash Flow", group = 1), linewidth = 1.2) +
    geom_point(aes(y = FreeCashFlow, color = "Free Cash Flow"), size = 2) +
    
    labs(
      title = "Operating Cash Flow vs Free Cash Flow",
      x = "Observation",
      y = "Billions",
      fill = "Bar Metric",
      color = "Line Metric"
    ) +
    scale_fill_manual(values = c("Operating Cash Flow" = "steelblue")) +
    scale_color_manual(values = c("Free Cash Flow" = "darkred")) +
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
 ############# Revenue Statement
  
## Total Revenue vs Total Expenses
output$TRev_TExPlot <- renderPlot({
  ggplot(Income_t_clean, aes(x = Observation)) +
  geom_line(aes(y = TotalRevenue, color = "TotalRevenue"), linewidth = 1) +
  geom_line(aes(y = TotalExpenses, color = "TotalExpenses"), linewidth = 1) +
  labs(title = "Revenue vs Expenses",  x = "Observation", y = "Billions",
    color = "Metric") +
  theme_minimal()
    }) 
## Step 1: Calculate Profit Margin

## Step 2: Reshape for side-by-side bars
income_long <- Income_t_factor %>%
  select(Observation, TotalRevenue, NetIncome, ProfitMargin) %>%
  pivot_longer(cols = c(TotalRevenue, NetIncome),
               names_to = "Metric", values_to = "Value")

## Step 3: Plot
output$revNetIncomePlot <- renderPlot({
  ggplot() +
    # Bars for Revenue & Net Income side by side
    geom_col(data = income_long,
             aes(x = Observation, y = Value, fill = Metric),
             position = position_dodge(width = 0.7), width = 0.6, alpha = 0.8) +
    
    # Profit Margin line
    geom_line(data = Income_t_factor,
              aes(x = Observation,
                  y = ProfitMargin * scale_factor / 100,
                  color = "Profit Margin", group = 1),
              linewidth = 1.2) +
    geom_point(data = Income_t_factor,
               aes(x = Observation,
                   y = ProfitMargin * scale_factor / 100,
                   color = "Profit Margin"),
               size = 2) +
    
    labs(
      title = "Revenue & Net Income vs Profit Margin",
      x = "Observation",
      y = "Billions ($)",
      fill = "Bar Metrics",
      color = "Line Metric"
    ) +
    scale_fill_manual(values = c("TotalRevenue" = "steelblue", "NetIncome" = "darkgreen")) +
    scale_color_manual(values = c("Profit Margin" = "firebrick")) +
    
    # Format y-axis
    scale_y_continuous(
      labels = scales::dollar_format(prefix = "$", suffix = "B"),
      sec.axis = sec_axis(~ . * 100 / scale_factor,
                          name = "Profit Margin (%)",
                          labels = function(x) paste0(round(x, 1), "%"))
    ) +
    theme_minimal()
})
}

# Run the app
shinyApp(ui = ui, server = server)
