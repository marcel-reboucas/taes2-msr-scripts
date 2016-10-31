require(qcc)
# install.packages("qcc")

setwd("/Users/Marcel/Google\ Drive/Mestrado/Aulas/TAES2/msr/data")

# Read data into the workspace
pdata <- read.csv(file = "out_summary_groupedByBuildId_v2.csv", header = TRUE, stringsAsFactors = FALSE)

colnames(pdata) <- c("Projeto","Nome","Email","Sucessos","Falhas","Total","Perc. sucesso","Casual?")
pdata$Total <- as.numeric(as.character(pdata$Total))
pareto.chart(pdata$Total)
hist(pdata$Total, breaks=40, col="red")