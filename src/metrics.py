import numpy as np


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
    
    if k < len(recommended_list):
        recommended_list = recommended_list[:k]

    flags = np.isin(bought_list, recommended_list)

    precision = flags.sum() / len(recommended_list)

    return precision


def money_precision_at_k(recommended_list, bought_list, prices_recommended, k=5):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)

    bought_list = bought_list  # Тут нет [:k] !!
    if k < len(recommended_list):
        recommended_list = recommended_list[:k]

    flags = np.isin(bought_list, recommended_list)

    # print(f"recommended_list: {recommended_list}")
    # print(f"bought_list: {bought_list}")
    # print(f"flags: {flags}")

    recommended_price = prices_recommended[prices_recommended['item_id'].isin(bought_list[flags])]
    bought_price = prices_recommended[prices_recommended['item_id'].isin(bought_list)]

    recommended_price_sum = recommended_price["sales_value"].sum()
    bought_price_sum = bought_price['sales_value'].sum()

    if bought_price_sum == 0:
        money_precision = 0
    else:
        money_precision = recommended_price_sum / bought_price_sum

    # print(f"recommended_price_sum: {recommended_price_sum}")
    # print(f"bought_price_sum: {bought_price_sum}")
    # print(f"money_precision: {money_precision}")

    return money_precision


def recall(recommended_list, bought_list):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)

    flags = np.isin(bought_list, recommended_list)

    recall = flags.sum() / len(bought_list)

    return recall


def recall_at_k(recommended_list, bought_list, k=5):

    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)

    if k < len(recommended_list):
        recommended_list = recommended_list[:k]

    flags = np.isin(bought_list, recommended_list)
    recall = flags.sum() / len(bought_list)

    return recall


def money_recall_at_k(recommended_list, bought_list, prices_recommended, prices_bought, k=5):
    # your_code

    return recall




# https://github.com/mike-chesnokov/x5_retailhero_2020_recs/commit/72b5a743a3652572cd52743effef357a74dabc5c

def normalized_average_precision(actual, recommended, k=30):
    actual = set(actual)
    if len(actual) == 0:
        return 0.0

    ap = average_precision(actual, recommended, k=k)
    ap_ideal = average_precision(actual, list(actual)[:k], k=k)
    return ap / ap_ideal


def run_queries(url, queryset_file):
    ap_values = []

    with open(queryset_file) as fin:
        for line in tqdm(fin):
            query_data, next_transaction = line.strip().split('\t')
            query_data = json.loads(query_data)
            next_transaction = json.loads(next_transaction)

            resp = requests.post(url, json=query_data, timeout=1)
            resp.raise_for_status()
            resp_data = resp.json()

            assert len(resp_data['recommended_products']) <= 30

            ap = normalized_average_precision(next_transaction['product_ids'], resp_data['recommended_products'])
            ap_values.append(ap)

    map_score = sum(ap_values) / len(ap_values)
    return map_score
