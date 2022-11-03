def undersampling(df, column, measure='mean', new_size=None):
    """For now it only works for two classes
    """
    import math
    import numpy as np
    def get_minority_class(df, column):
        # Obtaining classes
        classes = sorted(df[column].unique())

        # Amount of the class counts
        class_group = df[column].value_counts()
        if class_group.shape[0] != 2: raise ValueError('Implementado apenas para duas classes')

        return {
            'min': class_group.idxmin(),
            'max': class_group.idxmax(),
            'count_minor_class': class_group.min()
        }
    
    # Calculate the Euclidian Distance between a and b
    def euclidian_distance(x, y):
        return math.sqrt(((x - y) ** 2).sum())
    
    # get minor class
    classes_dic = get_minority_class(df, column)
    
    # define size of new dataset
    if not new_size: new_size = classes_dic['count_minor_class']
        
    # distributing the dataset
    minor_class_df = df[df[column] == classes_dic['min']]
    major_class_df = df[df[column] == classes_dic['max']]
    
    # representing the majority data set with the mean or variance
    if measure == 'var':
        applied_measure = major_class_df.var()
    elif measure == 'mean':
        applied_measure = major_class_df.mean()
    else:
        raise ValueError("Invalid measure!")
        
    # Calculate the distance of test and all elements of data train
    distances = major_class_df.apply(euclidian_distance, axis=1, **{'y': applied_measure})
    
    # getting k nearest neighbors (with k equal to new_size)
    k_nearest = distances.sort_values().iloc[:new_size]
    
    # Get the best set of records of size new.size
    best_subset = major_class_df.loc[k_nearest.index]
    
    return pd.concat([minor_class_df, best_subset], ignore_index=True)
