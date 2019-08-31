#  Undersampling Function to obtain the best subset of records from an unbalanced database when considered a 
# categorical variable of two classes, using Euclidean Distance.
undersampling.ed = function(original.data, variable.name, measure = "mean", optional.new.size = -1) {
  # Error meansure functions
  source("https://raw.githubusercontent.com/Genicleito/MATE10-Sistemas-Fuzzy/master/Trabalho/Codigos/error-measures.r")
  
  # identify the class with the smallest and largest number of records.
  define.minority.class = function(data, variable) {
    # obtaining classes
    classes = sort(unique(data[, variable]))
    
    # Amount minority class
    amount.minority.class = min(table(data[, variable]))
    
    class.group = table(data[, variable])
    
    max.class = classes[1]
    min.class = classes[2]
    if(class.group[ as.character(classes[1])] == amount.minority.class) {
      max.class = classes[2]
      min.class = classes[1]
    }
    
    # Return list with minor class, major class and records count of minor class
    list(min = min.class, max = max.class, count.minor.class = amount.minority.class)
  }
  
  # Calculate the Euclidian Distance between a and b
  euclidian.distance <- function(a, b) {
    sqrt(sum((a - b) ^ 2))
  }

  ############### calls of the functions defined above ###############
  classes = define.minority.class(original.data, variable.name)
  min.class = classes$min
  max.class = classes$max
  
  # define size of new dataset
  if (optional.new.size == -1) {
    new.size = classes$count.minor.class
  } else {
    new.size = optional.new.size
  }
  
  # distributing the dataset
  data.minor.class = original.data[original.data[, variable.name] == min.class, ]
  data.major.class = original.data[original.data[, variable.name] == max.class, ]
  
  # representing the majority data set with the mean or variance
  if(measure == "var")
    original.measure = apply(data.major.class, 2, var)
  else if(measure == "mean") {
    original.measure = apply(data.major.class, 2, mean)
  } else {
    cat("Invalid measure!\n")
    return(NULL)
  }
  
  # Calculate the distance of test and all elements of data train
  distances <- as.vector(apply(data.major.class, 1, euclidian.distance, original.measure))
  
  # getting k nearest neighbors (with k equal to new.size)
  k.nearest <- sort.list(distances)[1:new.size]
  
  # Get the best set of records of size new.size
  best.subset = data.major.class[k.nearest, ]
  
  # Returning the best subset obtained with Euclidian Distance
  rbind(data.minor.class, best.subset)
}


################################### Example of call ###################################

# # Load the dataset
# dataset = read.csv("[path].csv", header = T)
# 
# # time meansure of function call
# start.time <- Sys.time()
# 
# class.name = names(dataset)[length(dataset)]
# best.subset = undersampling.ed(dataset, class.name)
# end.time <- Sys.time()
# 
# print(end.time - start.time)
