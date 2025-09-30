from flask import Flask, request, jsonify, send_from_directory
import os
from algorithms import load_recipes, greedy_recipe_suggestions, gap_analysis, substitution_recommendations, build_ingredient_graph, suggest_complementary_ingredients, backtracking_recipe_combination

app = Flask(__name__, static_folder='../frontend')

recipes = load_recipes()

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

@app.route('/api/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    available = data.get('ingredients', [])
    use_backtracking = data.get('use_backtracking', False)
    graph = build_ingredient_graph(recipes)
    complements = suggest_complementary_ingredients(available, graph, recipes)
    if use_backtracking:
        combo = backtracking_recipe_combination(available, recipes)
        if combo:
            result = []
            for recipe in combo:
                gaps = gap_analysis(recipe, available)
                subs = substitution_recommendations(gaps, recipe)
                result.append({
                    'name': recipe['name'],
                    'matching': len(set(recipe['ingredients']) & set(available)),
                    'total': len(recipe['ingredients']),
                    'gaps': gaps,
                    'substitutions': subs,
                    'instructions': recipe['instructions']
                })
            return jsonify({
                'suggestions': result,
                'type': 'backtracking_combo',
                'complementary_ingredients': complements
            })
    suggestions = greedy_recipe_suggestions(available, recipes)
    result = []
    for sug in suggestions:
        recipe = sug['recipe']
        gaps = gap_analysis(recipe, available)
        subs = substitution_recommendations(gaps, recipe)
        result.append({
            'name': recipe['name'],
            'matching': sug['matching_count'],
            'total': sug['total_ingredients'],
            'enhanced_score': sug.get('enhanced_score', 0),
            'gaps': gaps,
            'substitutions': subs,
            'instructions': recipe['instructions']
        })
    return jsonify({
        'suggestions': result,
        'type': 'greedy',
        'complementary_ingredients': complements
    })

if __name__ == '__main__':
    app.run(debug=True)