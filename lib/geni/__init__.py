def ind_outlier(df, columns=None):
    """Cria coluna(s) que indica(m) se os valores em `columns` são outliers.
    """
    if (columns and isinstance(columns, str)): columns = [columns]
    df_describe = df[columns].describe()
    for col in df_describe.columns:
        serie = df_describe[col]
        fiq = serie.loc['75%'] - serie.loc['25%']
        l_sup = serie ['mean'] + (1.5 * fiq)
        l_inf = serie ['mean'] - (1.5 * fiq)
        df = df.assign(**{f'ind_outlier_{col}': np.where(((df[col] > l_sup) | (df[col] < l_inf)), 1, 0)})
    return df