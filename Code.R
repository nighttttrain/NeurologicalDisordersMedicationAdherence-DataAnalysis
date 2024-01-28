library(dplyr)
library(tidyr)
library(factoextra)
library(caret)
#read csv
OSF <- read.csv("OSF_csv1.csv", header = TRUE)
# select columns (6 indicator (Ng & Khor, 2017))
OSF_sams <- subset(OSF, select = c("sam_1","sam_2","sam_3","sams_4","sam_5",
                                   "sam_6","sam_7","sam_8","sam_9","sam_10",
                                   "sam_11","sam_12","sam_13","sam_14",
                                   "sam_15","sam_16","sam_17","sam_18"))
OSF_sams <- drop_na(OSF_sams)
# cluster after PCA
# read sav
library(haven)
OSF3 <- read_sav("/Users/rain/Downloads/OSF3 (1).sav")
# cluster 
OSF_sav1 <- subset(OSF_sav, select = c("FAC1_3","FAC2_3","FAC3_3",
                                       "sams_status_binary"))
OSF_sav1 <- drop_na(OSF_sav1)
OSF_sav1 <- OSF_sav1[OSF_sav1$sams_status_binary != 0, ]
OSF_sav1 <- subset(OSF_sav1, select = c("FAC1_3","FAC2_3","FAC3_3"))
OSF_sav1 <- scale(OSF_sav1)
km.out <- kmeans(OSF_sav1, centers = 3, nstart = 25)
## keep "0"
OSF_sav2 <- drop_na(OSF_sav1)
km.out <- OSF_sav2 %>% 
  filter(sams_status_binary != 0) %>%
  select(FAC1_3,FAC2_3,FAC2_3) %>%
  kmeans(centers = 3, nstart = 25) ##
km.out$size
fviz_cluster(labelsize = 8,
             ggtheme = theme_minimal(),
             list(data = OSF_sams1, clusters = km.clusters))
km.out_centers <- data.frame(km.out$centers)
km.out_cluster <- data.frame(km.clusters)
###3### clustering
# remove non-number 

# remove column that no need in cluster

# scale the data
OSF_sams1 <- scale(OSF_sams)
# calculate th number of clusters
fviz_nbclust(OSF_sams1, kmeans, method = "wss", k.max = 20, nstart=10) +
  labs(subtitle = "Elbow Method")
km.out_centers <- data.frame(km.out$centers)
# kmeans
km.out <- kmeans(OSF_sams1, centers = 5, nstart = 25)
  kmeans(centers = 3)
km.out$size #
# visualization # #3# the clustering result PCA
km.clusters <- km.out$cluster
rownames(top_500_data1) <- top_500_data$Symbol
fviz_cluster(labelsize = 8,
             ggtheme = theme_minimal(),
             list(data = OSF_sams1, clusters = km.clusters))
km.out_centers <- data.frame(km.out$centers)
km.out_cluster <- data.frame(km.clusters)


# generate a new column, calculate the highest from PCA
# fixed value & sams_4
OSF_sav$group <- max.col(subset(OSF, select =c("FAC1_3","FAC2_3","FAC3_3")), ties.method = "first")
OSF_sav$group <- ifelse(OSF_sav$FAC1_3 > OSF_sav$FAC2_3 & 
                          OSF_sav$FAC1_3 > OSF_sav$FAC3_3, 1, NA)
OSF_sav$group <- ifelse(OSF_sav$sams_status_binary == 0 ,0, 
                        ifelse(OSF_sav$FAC1_3 > OSF_sav$FAC2_3 & 
                                 OSF_sav$FAC1_3 > OSF_sav$FAC3_3,
                               1,
                               ifelse(OSF_sav$FAC2_3 > OSF_sav$FAC3_3, 2, 3)))

write_sav(OSF_sav, "output_OSF.sav")
write.csv(OSF_sav, file = "output_file.csv", row.names = FALSE)
# original values
OSF_sav$pca_group <- ifelse(OSF_sav$sams_status_binary == 0 ,0, 
                        ifelse(OSF_sav$FAC1_2 > OSF_sav$FAC2_2 & 
                                 OSF_sav$FAC1_2 > OSF_sav$FAC3_2,
                               1,
                               ifelse(OSF_sav$FAC2_2 > OSF_sav$FAC3_2, 2, 3)))

print(sum(is.na(OSF_sav$pca_group)))
print(table(OSF_sav$pca_group))
write_sav(OSF_sav, "output_OSF.sav")
write.csv(OSF_sav, file = "output_file.csv", row.names = FALSE)

# fixed value from SPSS pca
# read sav
OSF2_sav <- read_sav("OSF2.sav")
OSF2_sav$adherence_group <- ifelse(OSF2_sav$adherence_fix == 0 ,0, 
                            ifelse(OSF2_sav$FAC1_4 > OSF2_sav$FAC2_4 & 
                                     OSF2_sav$FAC1_4 > OSF2_sav$FAC3_4,
                                   1,
                                   ifelse(OSF2_sav$FAC2_4 > OSF2_sav$FAC3_4, 2, 3)))

print(sum(is.na(OSF2_sav$adherence_group)))
print(table(OSF2_sav$adherence_group))
write_sav(OSF2_sav, "OSF3.sav")

# descriptive
# bar chart
library(ggplot2)
ggplot(OSF3, aes())

df_bar <- data.frame(
  supp = c("adherence", "adherence", "adherence_fixed", "adherence_fixed"),
  Legend = c("Yes", "No", "Yes", "No"),
  len= c(168, 684, 192, 718))
# Define the custom order of categories
bar_order <- c("Yes", "No")
# Use factor() to create an ordered factor with the custom order
df_bar$Legend <- factor(df_bar$Legend, levels = bar_order)
  
ggplot(df_bar, aes(x=supp, y=len, fill=Legend)) +
  geom_bar(stat='identity', position='dodge')+
  labs(title = "Patient's Medication Adherence (Binary)", 
       x = "Medication Adherence", 
       y = "Numer of Patient")+
  theme_minimal()+
  theme(plot.title = element_text(hjust = 0.5))+
  geom_text(aes(label=len), vjust=1.6, color="white",
            position = position_dodge(1), size=3.5)+
  scale_fill_manual("legend", 
                    values = c("Yes" = "#1F78B4", "No" = "#A6CEE3"))
library(factoextra)  
# pie chart

df_pie <- data.frame(
  group = c("Full adherence", "Intentionality", "Missing knowledge", "Forgetfulness"),
  value = c(192, 183, 204, 328))

data <- data.frame(
  category = c("Category 3", "Category 1", "Category 4", "Category 2"),
  value = c(30, 20, 15, 35)
)
# Define the custom order of categories
custom_order <- c("Full adherence", "Intentionality", "Missing knowledge", "Forgetfulness")
# Use factor() to create an ordered factor with the custom order
df_pie$group <- factor(df_pie$group, levels = custom_order)

ggplot(df_pie, aes(x="", y=value, fill=group))+
  geom_bar(width = 1, stat = "identity")+
  coord_polar(theta = "y")+
  theme(axis.text = element_blank(),
        axis.ticks = element_blank(),
        panel.background = element_blank())+
  labs(title = "Patient's Medication Adherence Type")+
  scale_fill_brewer(palette="Blues")+
  theme_minimal()+
  theme_void()+
  theme(plot.title = element_text(hjust = 1.8))


# bar chart independent
library(readxl)
bar <- read_excel("independent.xlsx", col_names = FALSE)
# order
bar_order <- c("Male", "Female")
bar_order <- c("Age 55 - 64", "Age 65 - 74", "Age 75 - 84", "Age 85+")
bar_order <- c("Married", "Not married")
bar_order <- c("High", "Middle", "Low")
bar_order <- c("Cerebrovascular", "Epilepsy", 
               "Movement (PDs)", 
               "Neuromuscular",
               "Miscellaneous")
bar_order <- c("Independent", "Needs help from others")
bar_order <- c("No", "Yes")
bar_order <- c("Agreeableness", "Conscientiousness", "Extraversion",
               "Neuroticism", "Openness")
bar_order <- c("Q8","Q9","Q10","Q11","Q12","Q13","Q17")
bar_order <- c("Q1","Q2","Q3","Q4","Q5")
bar_order <- c("Q6","Q14","Q15","Q16","Q18")
bar$...1 <- factor(bar$...1, levels = bar_order)

ggplot(data=bar, aes(x=...1, y=...2)) +
  geom_bar(stat="identity", width=0.7, fill="#AED8E6",
           position=position_dodge(.7))+
  geom_text(aes(label=...2), vjust=1.5, color="white", size=4.5)+
  theme_minimal()+
  labs(title = "Bar Chart of SAMS for Non-adherence Group 3", 
     x = "SAMS Questionnaire", 
     y = "Numer of Patient")+
  theme(plot.title = element_text(hjust = 0.5))

