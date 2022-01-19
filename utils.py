def prefilter_items(data, interesting_cats, item_features,):
    # Уберем самые популярные товары (их и так купят)
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    
    # Уберем товары, которые не продавались за последние 12 месяцев
    data = data.loc[data['week_no'] > (max(data['week_no']) - 52)]

    
    # Уберем не интересные для рекоммендаций категории (department)
    data = data.loc[data['item_id'].isin(item_features.loc[item_features['department'].isin(interesting_cats)]['item_id'].unique())]
    
    # # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб. 
    # data = data.loc[data['price'] > data['price'].quantile(0.05)]
    # # Уберем слишком дорогие товары
    # data = data.loc[data['price'] < data['price'].quantile(0.95)]
    return data
    
