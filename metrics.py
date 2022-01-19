


def hit_rate(recommended_list, bought_list):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    flags = np.isin(bought_list, recommended_list)
    
    hit_rate = (flags.sum() > 0) * 1
    
    return hit_rate


def hit_rate_at_k(recommended_list, bought_list, k=5):
    recommended_list = np.array(recommended_list[:k])
    flags = np.isin(bought_list, recommended_list)
    
    hit_rate = (flags.sum() > 0) * 1

    
    return hit_rate


def precision(recommended_list, bought_list):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    flags = np.isin(bought_list, recommended_list)
    
    precision = flags.sum() / len(recommended_list)
    
    return precision


def precision_at_k(recommended_list, bought_list, k=5):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    bought_list = bought_list  # Тут нет [:k] !!
    recommended_list = recommended_list[:k]
    
    flags = np.isin(bought_list, recommended_list)
    
    precision = flags.sum() / len(recommended_list)
    
    
    return precision


def money_precision_at_k(recommended_list, bought_list, prices_recommended, k=5):
    # создаем булеву маску покупок
    flags = np.isin(np.array(recommended_list[:k]), np.array(bought_list))
    # переводим булевы значения в целочисленные
    flags = list(map(int, flags))

    # считаем money precsision как деление скалярных произведений векторов  на векторы
    # скалярное произведение вектора покупок(маски) на вектор цен 
    bought = np.array(flags).dot(np.array(prices_recommended[:k]))

    # скалярное произведение вектора рекомендаций на вектор цен
    recommended = np.ones((len(prices_recommended[:k]))).dot(np.array(prices_recommended[:k])) 

    # money precision
    precision = bought / recommended
    

    
    return precision

def recall(recommended_list, bought_list):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    flags = np.isin(bought_list, recommended_list)
    
    recall = flags.sum() / len(bought_list)
    
    return recall


def recall_at_k(recommended_list, bought_list, k=5):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list[:k])
    
    flags = np.isin(bought_list, recommended_list)
    
    recall = flags.sum() / len(bought_list)
    # сделать дома
    
    return recall


def money_recall_at_k(recommended_list, bought_list, prices_recommended, prices_bought, k=5):
    # создаем булеву маску покупок
    flags = np.isin(np.array(bought_list), np.array(recommended_list[:k]), )
    # переводим булевы значения в целочисленные
    flags = list(map(int, flags))

    # считаем money precsision как деление скалярных произведений векторов  на векторы
    # скалярное произведение вектора покупок(маски) на вектор цен 
    bought_rekommended_k = np.array(flags).dot(np.array(prices_bought))

    # скалярное произведение вектора рекомендаций на вектор цен
    bought_price = np.ones((len(prices_bought))).dot(np.array(prices_bought)) 

    # money precision
    recall = bought_rekommended_k / bought_price
    # сделать дома
    
    return recall



def ap_k(recommended_list, bought_list, k=5):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)[:k]
    
    relevant_indexes = np.nonzero(np.isin(recommended_list, bought_list))[0]
    
    if len(relevant_indexes) == 0:
        return 0
    
    amount_relevant = len(relevant_indexes)
    
    sum_ = sum([precision_at_k(recommended_list, bought_list, k=index_relevant+1) for index_relevant in relevant_indexes])
    return sum_/amount_relevant
  


def map_k(recommended_list, bought_list, k=5):
    result = 0
    for rec, bougt in zip(recommended_list, bought_list):
        result += ap_k(rec, bougt, k=k)

    result = result / len(recommended_list)
    
    return result



def reciprocal_rank(recommended_list, bought_list, k=1):
    result = []
    for rec, bought in zip(recommended_list[:k], bought_list):
        relevant = np.isin(bought, rec)
        index_list = np.arange(1, len(relevant)+1,)
        ranks = [0 if rel == False else ind
            for ind, rel in zip(index_list, relevant)]

        res = [1/a for a in ranks if a!= 0]
    
        result.append(sum(res))
    return sum(result)

