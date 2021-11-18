import json
from collections import defaultdict

import math
from tqdm import tqdm

from config import Config

cfg = Config()


def load_meta(i):
    path = cfg.path_for_metadata(i)
    with open(path, 'r') as f:
        return json.load(f)


def calculate_rarity(meta_map: dict):
    rarity_map = defaultdict(lambda: defaultdict(float))
    for ident, data in meta_map.items():
        attrs = data['attributes']
        for name, value in attrs.items():
            rarity_map[name][value] += 1

    prob_rar_map = defaultdict(lambda: defaultdict(float))
    for attr_name, attr_counts in rarity_map.items():
        for kind, count in attr_counts.items():
            prob_rar_map[attr_name][kind] = count / cfg.N

    return prob_rar_map


def calculate_overall_rarity(meta: dict, rar_map: dict):
    r = 1.0
    for attr_name, attr_value in meta['attributes'].items():
        # probability of attr_name-attribute with value attr_value
        prob = rar_map[attr_name][attr_value]
        r *= prob
    return math.log(r)


def load_all_meta():
    try:
        with open(Config.PATH_ALL_META, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def load_all_meta_map_from_disk(from_scratch=False):
    meta_map = {} if from_scratch else load_all_meta().get('map', {})
    if not from_scratch:
        print(f'Loaded {len(meta_map)} items...')

    return meta_map


def update_js_rank_list(ranks):
    with open(Config.PATH_ONLY_RANKS_JS, 'w') as f:
        json_str = json.dumps(ranks, indent=4)
        f.write(f"const RANKS = {json_str};\n")


def convert_one_meta(meta):
    name: str = meta['name']
    ident = int(name.split('#')[1])
    attributes = meta['attributes']

    attributes = {x['trait_type']: x['value'] for x in attributes}

    pic_url = meta['image']
    return {
        'id': ident,
        'attributes': attributes,
        'pic': pic_url,
    }


def calculate_stats(meta_map):
    rarity_prob_map = calculate_rarity(meta_map)

    for meta in meta_map.values():
        meta['prob'] = calculate_overall_rarity(meta, rarity_prob_map)

    # ranking
    place = 1
    only_ranks = {}
    for meta in sorted(meta_map.values(), key=lambda meta: meta['prob']):
        meta['rank'] = place
        only_ranks[meta['id']] = place
        place += 1

    return {
               'map': meta_map,
               'rarity': rarity_prob_map,
           }, only_ranks


def save_stats_and_ranks(data, only_ranks):
    with open(cfg.PATH_ALL_META, 'w') as f:
        json.dump(data, f, indent=2)

    with open(cfg.PATH_ONLY_RANKS, 'w') as f:
        json.dump(only_ranks, f, indent=2)


def run_convert_metadata(meta_map):
    all_meta_data, only_ranks = calculate_stats(meta_map)
    save_stats_and_ranks(all_meta_data, only_ranks)
    update_js_rank_list(only_ranks)

