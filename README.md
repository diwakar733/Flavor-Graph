# FlavorGraph - Intelligent Recipe Navigator

FlavorGraph is a web application that intelligently suggests recipes based on available ingredients, using advanced algorithms like greedy search, backtracking, and graph theory to provide personalized and efficient recommendations.

## Features

- **Recipe Suggestions**: Input available ingredients and get tailored recipe suggestions.
- **Gap Analysis**: Identifies missing ingredients for suggested recipes.
- **Substitution Recommendations**: Suggests ingredient substitutions for missing items.
- **Complementary Ingredients**: Recommends additional ingredients that pair well with what you have.
- **Algorithm Selection**: Choose between greedy (fast, approximate) and backtracking (precise, exact) modes.
- **Graph-Enhanced Scoring**: Uses ingredient relationships to prioritize better recipes.
- **Varied Results**: Randomization ensures different suggestions on repeated queries.
- **Modern UI**: Responsive design with cards, gradients, and smooth animations.

## Algorithms Used

### Greedy Algorithm
- **Location**: `algorithms.py` - `greedy_recipe_suggestions()` function
- **Detailed Explanation**:
  - **Workflow**: The function iterates through all recipes in the dataset. For each recipe, it computes the intersection between the user's available ingredients and the recipe's required ingredients to find matching ones. It then applies a graph-enhanced score by checking how many pairs of matching ingredients co-occur in other recipes, adding a small bonus for each connected pair to prioritize synergistic combinations. Recipes are sorted by this score in descending order, with randomization applied to break ties and ensure variety on repeated runs. Finally, it returns the top 5 recipes as suggestions.
  - **Why Used**: This is the default algorithm for providing fast, approximate recipe suggestions. It's efficient for large datasets and gives good results when users have partial ingredients, making it ideal for everyday use without long wait times.
  - **Benefits**: Quick response, varied outputs, smarter prioritization through graph bonuses.
  - **Limitations**: May not find exact matches; approximations only.
  - **Integration**: Called in `app.py` when `use_backtracking` is false, enhancing user experience with intelligent scoring.

### Backtracking Algorithm
- **Location**: `algorithms.py` - `backtracking_recipe_combination()` function
- **Detailed Explanation**:
  - **Workflow**: This recursive function explores all possible subsets of recipes to find one where the combined ingredients exactly match the user's available set (no missing or extra ingredients). It starts with an empty combination and for each recipe, decides to include or exclude it. If included, it checks if the recipe's ingredients are a subset of available ones, updates the used ingredients set, and recurses. At the end of recipes, it verifies if used ingredients equal available; if yes, returns the combination. If no exact match is found after exploring, it returns None, triggering fallback to greedy.
  - **Why Used**: Provides precise, waste-minimizing suggestions when users want to use exactly what they have. It's toggled via the UI checkbox for users who prefer accuracy over speed.
  - **Benefits**: Exact matches, no leftovers, optimal for small ingredient sets.
  - **Limitations**: Exponential time complexity makes it slow for large recipe datasets; may not always find a match.
  - **Integration**: Invoked in `app.py` when `use_backtracking` is true, offering an alternative mode for detailed users.

### Graph Theory
- **Location**: `algorithms.py` - `build_ingredient_graph()`, `graph_enhanced_score()`, `suggest_complementary_ingredients()`
- **Detailed Explanation**:
  - **Workflow**: The graph is built by mapping each ingredient to the set of recipes it appears in, creating implicit connections. For scoring, it boosts recipe scores based on ingredient pairs that share recipes. For complements, it scans recipes containing available ingredients, counts missing ones that frequently co-occur, and ranks them to suggest additions.
  - **Why Used**: Adds intelligence by leveraging ingredient relationships, improving suggestion quality beyond simple counts.
  - **Benefits**: Enhances recommendations with real-world patterns, suggests useful additions.
  - **Limitations**: Requires pre-built graph, adds computation.
  - **Integration**: Used in greedy suggestions and complement features, making the app more insightful.

## Project Structure

```
FlavorGraph/
├── backend/
│   ├── app.py              # Flask server with API routes
│   ├── algorithms.py       # Core algorithms (greedy, backtracking, graph)
│   └── recipes.json        # Sample recipe dataset (~50 recipes)
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # CSS styles with modern design
│   └── script.js           # JavaScript for UI interactions and API calls
├               
└── README.md               # This file
```

## Installation

1. Ensure Python 3.7+ is installed.
2. Install Flask: `pip install flask`
3. Clone or download the project.
4. Navigate to the `FlavorGraph/backend` directory.
5. Run the app: `python app.py`

The app will start on `http://127.0.0.1:5000`.

## Usage

1. Open `http://127.0.0.1:5000` in your browser.
2. Enter available ingredients in the textarea (comma-separated, e.g., "chicken, rice, onions").
3. Optionally check "Use Backtracking" for exact combinations.
4. Click "Get Recipe Suggestions".
5. View suggested recipes with matching info, gaps, substitutions, and instructions.
6. See complementary ingredients for more options.

## API Endpoints

- `GET /`: Serves the main page.
- `POST /api/suggest`: Accepts JSON with `ingredients` (list) and `use_backtracking` (bool). Returns suggestions, type, and complements.

Example request:
```json
{
  "ingredients": ["chicken", "rice", "onions"],
  "use_backtracking": false
}
```

## Dataset

The `recipes.json` contains ~50 sample recipes with:
- Name
- Ingredients (list)
- Instructions (string)
- Substitutions (dict, optional)

You can expand this dataset for more recipes.

## Technologies

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Algorithms**: Custom implementations in Python

## Example: How Algorithms Work in FlavorGraph

Suppose a user has available ingredients: "chicken, rice, onions, garlic".

### Greedy Algorithm (Default Mode)
- **Process**: Scans all recipes, finds matches like "Chicken Stir Fry" (matches: chicken, onions, garlic - 3/4), "Chicken Noodle Soup" (matches: chicken, onions, garlic - 3/5), etc. Enhances scores with graph bonuses (e.g., chicken and garlic often pair, adding points). Sorts and returns top 5, e.g., Chicken Stir Fry, Chicken Noodle Soup, etc.
- **Helpfulness**: Provides quick, varied suggestions even with partial ingredients. User gets immediate options without waiting, ideal for busy cooks.
- **Output**: Suggests recipes with gaps (e.g., missing bell peppers for Stir Fry) and substitutions (e.g., use shallots for onions).

### Backtracking Algorithm (When Toggled)
- **Process**: Explores subsets to find exact match. For "chicken, rice, onions, garlic", it might find a combination like "Chicken Stir Fry" + "Garlic Rice" if their ingredients exactly cover the set. If no exact combo, falls back to greedy.
- **Helpfulness**: Ensures no waste by using exactly available ingredients, perfect for users with limited supplies or wanting precise planning.
- **Output**: Returns a combo of recipes that use all ingredients, or greedy if none found.

Both algorithms make FlavorGraph efficient and user-friendly, with greedy for speed and backtracking for precision.

## Contributing

Feel free to enhance the algorithms, add more recipes, or improve the UI. Ensure changes maintain the core functionality.

