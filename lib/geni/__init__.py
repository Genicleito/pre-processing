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

def series_to_supervised(df, n_prev=1, n_later=0, cols_fut=None, dropna=True, partition_by=None, sort_by=None, debug=True):
    # cols_fut examle: {'<column_name>': <qtd_future_shift>, '<column_name>': <qtd_future_shift>}
    if debug: from tqdm import tqdm
    if n_later != 0: cols_fut = None
    columns = df.columns
    df_result = pd.DataFrame()
    dfs_flt = [df] if not partition_by else [x.query(f'{partition_by} == "{value}"') for x in df[partition_by].unique()]
    for df_flt in (dfs_flt if not debug else tqdm(dfs_flt)):
        if sort_by: df_flt.sort_values(by=sort_by)
        dfs = [df_flt.rename(columns={col: f'{col}_t-{j}' for col in columns}).shift(j) for j in range(1, n_prev + 1)]
        dfs += [df_flt]
        dfs += [df_flt.rename(columns={col: f'{col}_t+{j+1}' for col in columns}).shift(-(j+1)) for j in range(n_later)]
        if cols_fut:
            i_df = -2 if n_later > 0 else -1
            dfs[i_df] = dfs[i_df].assign(**{
                f'{x}_t+{j+1}': dfs[i_df][x].shift(-(j+1)) for x in cols_fut.keys() for j in range(cols_fut[x])
            })
        df_result = df_result.append(
            pd.concat(dfs, axis=1).dropna() if dropna else pd.concat(dfs, axis=1),
            ignore_index=True
        )
    return df_result
