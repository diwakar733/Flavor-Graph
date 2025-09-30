import json
import random
from collections import defaultdict

def load_recipes():
    with open('recipes.json', 'r') as f:
        return json.load(f)

def build_ingredient_graph(recipes):
    graph = defaultdict(set)
    for recipe in recipes:
        for ing in recipe['ingredients']:
            graph[ing].add(recipe['name'])
    return graph

def graph_enhanced_score(available_ingredients, recipe, graph):
    base_score = len(set(recipe['ingredients']) & set(available_ingredients))
    connection_bonus = sum(1 for ing in recipe['ingredients'] if ing in available_ingredients and len(graph[ing]) > 1)
    return base_score + (connection_bonus * 0.5)

def greedy_recipe_suggestions(available_ingredients, recipes, top_n=5):
    graph = build_ingredient_graph(recipes)
    suggestions = []
    for recipe in recipes:
        matching = set(recipe['ingredients']) & set(available_ingredients)
        score = graph_enhanced_score(available_ingredients, recipe, graph)
        if len(matching) > 0:
            suggestions.append({
                'recipe': recipe,
                'matching_count': len(matching),
                'total_ingredients': len(recipe['ingredients']),
                'enhanced_score': score
            })
    # Sort by enhanced score descending, then randomize for ties
    suggestions.sort(key=lambda x: (-x['enhanced_score'], random.random()))
    return suggestions[:top_n]

def backtracking_recipe_combination(available, recipes, index=0, current_combo=[], used_ing=set()):
    if index == len(recipes):
        return current_combo if used_ing == set(available) else None
    # Skip
    result = backtracking_recipe_combination(available, recipes, index+1, current_combo, used_ing)
    if result:
        return result
    # Include
    recipe = recipes[index]
    recipe_ing = set(recipe['ingredients'])
    if recipe_ing.issubset(set(available)):
        new_used = used_ing | recipe_ing
        result = backtracking_recipe_combination(available, recipes, index+1, current_combo + [recipe], new_used)
        if result:
            return result
    return None

def gap_analysis(recipe, available):
    missing = set(recipe['ingredients']) - set(available)
    return list(missing)

def substitution_recommendations(missing, recipe):
    subs = {}
    for ing in missing:
        if ing in recipe.get('substitutions', {}):
            subs[ing] = recipe['substitutions'][ing]
    return subs

def suggest_complementary_ingredients(available_ingredients, graph, recipes, top_n=3):
    complements = defaultdict(int)
    for ing in available_ingredients:
        if ing in graph:
            for connected_recipe_name in graph[ing]:
                connected_recipe = next((r for r in recipes if r['name'] == connected_recipe_name), None)
                if connected_recipe:
                    for other_ing in connected_recipe['ingredients']:
                        if other_ing != ing and other_ing not in available_ingredients:
                            complements[other_ing] += 1
    sorted_complements = sorted(complements.items(), key=lambda x: x[1], reverse=True)
    return [ing for ing, count in sorted_complements[:top_n]]

# For graph theory: perhaps shortest path or something, but for now, use above.