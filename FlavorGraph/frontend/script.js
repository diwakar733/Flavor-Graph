document.getElementById('suggest-btn').addEventListener('click', async () => {
    const input = document.getElementById('ingredients-input').value.trim();
    if (!input) {
        alert('Please enter some ingredients.');
        return;
    }
    const ingredients = input.split(',').map(i => i.trim().toLowerCase()).filter(i => i);

    const btn = document.getElementById('suggest-btn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const complementsSection = document.getElementById('complements-section');
    const complementsDiv = document.getElementById('complements');

    btn.disabled = true;
    btn.textContent = 'Generating...';
    loading.style.display = 'block';
    results.innerHTML = '';
    complementsSection.style.display = 'none';

    try {
        const useBacktracking = document.getElementById('backtracking-toggle').checked;
        const response = await fetch('/api/suggest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ingredients, use_backtracking: useBacktracking })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        displayResults(data.suggestions);
        displayComplements(data.complementary_ingredients);
    } catch (error) {
        console.error('Error:', error);
        results.innerHTML = '<div class="no-results">An error occurred. Please try again.</div>';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Get Recipe Suggestions';
        loading.style.display = 'none';
    }
});

function displayResults(suggestions) {
    const resultsDiv = document.getElementById('results');
    if (suggestions.length === 0) {
        resultsDiv.innerHTML = '<div class="no-results">No recipes found with your ingredients. Try adding more!</div>';
        return;
    }

    resultsDiv.innerHTML = suggestions.map(sug => `
        <div class="recipe-card">
            <img src="https://via.placeholder.com/300x200/3498db/white?text=${encodeURIComponent(sug.name)}" alt="${sug.name}">
            <h3>${sug.name}</h3>
            <div class="match-info">Matching: ${sug.matching}/${sug.total} ingredients (Score: ${sug.enhanced_score.toFixed(1)})</div>
            ${sug.gaps.length > 0 ? `<div class="gaps">Missing: ${sug.gaps.join(', ')}</div>` : '<div class="match-info">All ingredients available!</div>'}
            ${Object.keys(sug.substitutions).length > 0 ? `<div class="subs">Suggestions: ${Object.entries(sug.substitutions).map(([k,v]) => `${k} → ${v}`).join(', ')}</div>` : ''}
            <div class="instructions">${sug.instructions}</div>
        </div>
    `).join('');
}

function displayComplements(complements) {
    const complementsSection = document.getElementById('complements-section');
    const complementsDiv = document.getElementById('complements');
    if (complements.length === 0) {
        complementsSection.style.display = 'none';
        return;
    }
    complementsDiv.innerHTML = `
        <div class="complements-list">
            ${complements.map(ing => `<span class="complement-tag">${ing}</span>`).join('')}
        </div>
        <p>These ingredients pair well with what you have—consider adding them for more options!</p>
    `;
    complementsSection.style.display = 'block';
}