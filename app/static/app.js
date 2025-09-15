document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('request-form');
  const resultsEl = document.getElementById('results');
  const inventoryEl = document.getElementById('inventory');

  // Prefill inventory with the same items used in tests
  const defaultInventory = [
    // Business casual / formal set
    {
      item_id: 'top1',
      item_type: 'top',
      name: 'Blue Dress Shirt',
      color: 'blue',
      material: 'cotton',
      size: 'M',
      style: ['formal', 'business'],
      weather_suitability: ['cool', 'mild', 'warm'],
      occasion_suitability: ['business_casual', 'casual'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'bottom1',
      item_type: 'bottom',
      name: 'Black Dress Pants',
      color: 'black',
      material: 'wool',
      size: '32',
      style: ['formal', 'business'],
      weather_suitability: ['cool', 'mild'],
      occasion_suitability: ['business_casual', 'casual'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'shoes1',
      item_type: 'shoes',
      name: 'Black Leather Shoes',
      color: 'black',
      material: 'leather',
      size: '42',
      style: ['formal', 'classic'],
      weather_suitability: ['cool', 'mild'],
      occasion_suitability: ['business_casual', 'casual'],
      is_clean: true,
      metadata: {}
    },

    // Casual set
    {
      item_id: 'top2',
      item_type: 'top',
      name: 'White T-Shirt',
      color: 'white',
      material: 'cotton',
      size: 'M',
      style: ['casual', 'minimalist'],
      weather_suitability: ['warm', 'hot', 'mild'],
      occasion_suitability: ['casual'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'bottom2',
      item_type: 'bottom',
      name: 'Dark Blue Jeans',
      color: 'blue',
      material: 'denim',
      size: '32',
      style: ['casual'],
      weather_suitability: ['cool', 'mild', 'warm'],
      occasion_suitability: ['casual'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'shoes2',
      item_type: 'shoes',
      name: 'White Sneakers',
      color: 'white',
      material: 'synthetic',
      size: '42',
      style: ['casual', 'minimalist'],
      weather_suitability: ['mild', 'warm', 'hot'],
      occasion_suitability: ['casual'],
      is_clean: true,
      metadata: {}
    },

    // Rainy / outerwear
    {
      item_id: 'outer1',
      item_type: 'outerwear',
      name: 'Navy Raincoat',
      color: 'navy',
      material: 'polyester',
      size: 'M',
      style: ['casual', 'classic'],
      weather_suitability: ['rainy', 'cool', 'cold'],
      occasion_suitability: ['casual', 'business_casual'],
      is_clean: true,
      metadata: {}
    },

    // Party set
    {
      item_id: 'top3',
      item_type: 'top',
      name: 'Black Silk Shirt',
      color: 'black',
      material: 'silk',
      size: 'M',
      style: ['party', 'formal'],
      weather_suitability: ['mild', 'warm'],
      occasion_suitability: ['party', 'formal'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'bottom3',
      item_type: 'bottom',
      name: 'Slim Chinos',
      color: 'khaki',
      material: 'cotton',
      size: '32',
      style: ['casual', 'smart_casual'],
      weather_suitability: ['mild', 'warm'],
      occasion_suitability: ['party', 'business_casual', 'casual'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'shoes3',
      item_type: 'shoes',
      name: 'Brown Brogues',
      color: 'brown',
      material: 'leather',
      size: '42',
      style: ['classic', 'business'],
      weather_suitability: ['mild', 'cool'],
      occasion_suitability: ['business_casual', 'party'],
      is_clean: true,
      metadata: {}
    },

    // Sport set
    {
      item_id: 'top4',
      item_type: 'top',
      name: 'Moisture-Wicking Tee',
      color: 'gray',
      material: 'polyester',
      size: 'M',
      style: ['sport'],
      weather_suitability: ['warm', 'hot'],
      occasion_suitability: ['sporty'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'bottom4',
      item_type: 'bottom',
      name: 'Running Shorts',
      color: 'black',
      material: 'synthetic',
      size: 'M',
      style: ['sport'],
      weather_suitability: ['warm', 'hot'],
      occasion_suitability: ['sporty'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'shoes4',
      item_type: 'shoes',
      name: 'Running Shoes',
      color: 'blue',
      material: 'mesh',
      size: '42',
      style: ['sport'],
      weather_suitability: ['mild', 'warm', 'hot'],
      occasion_suitability: ['sporty'],
      is_clean: true,
      metadata: {}
    },

    // Cold weather boots
    {
      item_id: 'shoes5',
      item_type: 'shoes',
      name: 'Black Chelsea Boots',
      color: 'black',
      material: 'leather',
      size: '42',
      style: ['classic'],
      weather_suitability: ['cold', 'cool', 'mild'],
      occasion_suitability: ['business_casual', 'casual', 'party'],
      is_clean: true,
      metadata: {}
    },

    // Evening set
    {
      item_id: 'top5',
      item_type: 'top',
      name: 'Navy Dress Shirt',
      color: 'navy',
      material: 'cotton',
      size: 'M',
      style: ['formal', 'evening'],
      weather_suitability: ['cool', 'mild', 'warm'],
      occasion_suitability: ['evening', 'formal'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'bottom5',
      item_type: 'bottom',
      name: 'Charcoal Dress Pants',
      color: 'gray',
      material: 'wool',
      size: '32',
      style: ['formal', 'evening'],
      weather_suitability: ['cool', 'mild'],
      occasion_suitability: ['evening', 'formal'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'shoes6',
      item_type: 'shoes',
      name: 'Patent Leather Oxfords',
      color: 'black',
      material: 'leather',
      size: '42',
      style: ['formal', 'evening'],
      weather_suitability: ['cool', 'mild', 'warm'],
      occasion_suitability: ['evening', 'formal'],
      is_clean: true,
      metadata: {}
    },

    // Beach set
    {
      item_id: 'top6',
      item_type: 'top',
      name: 'White Linen Shirt',
      color: 'white',
      material: 'linen',
      size: 'M',
      style: ['casual', 'beach'],
      weather_suitability: ['warm', 'hot'],
      occasion_suitability: ['beach', 'casual'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'bottom6',
      item_type: 'bottom',
      name: 'Beige Shorts',
      color: 'beige',
      material: 'cotton',
      size: 'M',
      style: ['casual', 'beach'],
      weather_suitability: ['warm', 'hot'],
      occasion_suitability: ['beach', 'casual'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'shoes7',
      item_type: 'shoes',
      name: 'Flip Flops',
      color: 'black',
      material: 'rubber',
      size: '42',
      style: ['casual', 'beach'],
      weather_suitability: ['warm', 'hot'],
      occasion_suitability: ['beach'],
      is_clean: true,
      metadata: {}
    },

    // Rainy footwear
    {
      item_id: 'shoes8',
      item_type: 'shoes',
      name: 'Rain Boots',
      color: 'black',
      material: 'rubber',
      size: '42',
      style: ['casual', 'classic'],
      weather_suitability: ['rainy', 'cold', 'cool'],
      occasion_suitability: ['casual', 'business_casual'],
      is_clean: true,
      metadata: {}
    },

    // Cold outerwear
    {
      item_id: 'outer2',
      item_type: 'outerwear',
      name: 'Wool Overcoat',
      color: 'black',
      material: 'wool',
      size: 'M',
      style: ['classic', 'formal'],
      weather_suitability: ['cold', 'cool'],
      occasion_suitability: ['formal', 'evening', 'business_casual'],
      is_clean: true,
      metadata: {}
    },
    // Casual cold-weather top and outerwear
    {
      item_id: 'top_casual_cold',
      item_type: 'top',
      name: 'Fleece Hoodie',
      color: 'navy',
      material: 'fleece',
      size: 'M',
      style: ['casual'],
      weather_suitability: ['cold', 'cool'],
      occasion_suitability: ['casual'],
      is_clean: true,
      metadata: {}
    },
    {
      item_id: 'outer_casual_cold',
      item_type: 'outerwear',
      name: 'Puffer Jacket',
      color: 'black',
      material: 'synthetic',
      size: 'M',
      style: ['casual'],
      weather_suitability: ['cold', 'cool'],
      occasion_suitability: ['casual'],
      is_clean: true,
      metadata: {}
    },
    // Accessory
    {
      item_id: 'acc1',
      item_type: 'accessory',
      name: 'Leather Belt',
      color: 'black',
      material: 'leather',
      size: 'L',
      style: ['classic', 'minimalist'],
      weather_suitability: ['cool', 'mild', 'warm', 'hot', 'cold', 'rainy'],
      occasion_suitability: ['business_casual', 'casual', 'formal', 'party'],
      is_clean: true,
      metadata: {}
    },

    // ==============================
    // All-occasion, all-weather core
    // These ensure at least one valid outfit for every combination
    // ==============================

    // Formal core
    { item_id: 'top_formal_all', item_type: 'top', name: 'All-Weather Formal Shirt', color: 'white', material: 'performance_cotton', size: 'M', style: ['formal'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['formal'], is_clean: true, metadata: {} },
    { item_id: 'bottom_formal_all', item_type: 'bottom', name: 'All-Weather Formal Trousers', color: 'charcoal', material: 'tech_wool', size: '32', style: ['formal'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['formal'], is_clean: true, metadata: {} },
    { item_id: 'shoes_formal_all', item_type: 'shoes', name: 'Waterproof Formal Oxfords', color: 'black', material: 'treated_leather', size: '42', style: ['formal'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['formal'], is_clean: true, metadata: {} },

    // Business Casual core
    { item_id: 'top_biz_all', item_type: 'top', name: 'All-Weather Oxford', color: 'light_blue', material: 'performance_cotton', size: 'M', style: ['business','classic'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['business_casual'], is_clean: true, metadata: {} },
    { item_id: 'bottom_biz_all', item_type: 'bottom', name: 'Stretch Chinos', color: 'navy', material: 'tech_cotton', size: '32', style: ['business','classic'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['business_casual'], is_clean: true, metadata: {} },
    { item_id: 'shoes_biz_all', item_type: 'shoes', name: 'All-Weather Derbies', color: 'brown', material: 'treated_leather', size: '42', style: ['classic','business'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['business_casual'], is_clean: true, metadata: {} },

    // Casual core
    { item_id: 'top_casual_all', item_type: 'top', name: 'Tech Tee', color: 'gray', material: 'performance_poly', size: 'M', style: ['casual','minimalist'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['casual'], is_clean: true, metadata: {} },
    { item_id: 'bottom_casual_all', item_type: 'bottom', name: 'All-Weather Jeans', color: 'dark_blue', material: 'tech_denim', size: '32', style: ['casual'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['casual'], is_clean: true, metadata: {} },
    { item_id: 'shoes_casual_all', item_type: 'shoes', name: 'Weatherproof Sneakers', color: 'white', material: 'treated_mesh', size: '42', style: ['casual','minimalist'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['casual'], is_clean: true, metadata: {} },

    // Sporty core
    { item_id: 'top_sporty_all', item_type: 'top', name: 'All-Weather Training Tee', color: 'black', material: 'performance_poly', size: 'M', style: ['sport'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['sporty'], is_clean: true, metadata: {} },
    { item_id: 'bottom_sporty_all', item_type: 'bottom', name: 'All-Weather Joggers', color: 'black', material: 'tech_poly', size: 'M', style: ['sport'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['sporty'], is_clean: true, metadata: {} },
    { item_id: 'shoes_sporty_all', item_type: 'shoes', name: 'Trail Running Shoes', color: 'gray', material: 'treated_mesh', size: '42', style: ['sport'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['sporty'], is_clean: true, metadata: {} },

    // Evening core
    { item_id: 'top_evening_all', item_type: 'top', name: 'Evening Dress Shirt (All-Weather)', color: 'black', material: 'performance_cotton', size: 'M', style: ['evening','formal'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['evening'], is_clean: true, metadata: {} },
    { item_id: 'bottom_evening_all', item_type: 'bottom', name: 'Evening Dress Trousers', color: 'black', material: 'tech_wool', size: '32', style: ['evening','formal'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['evening'], is_clean: true, metadata: {} },
    { item_id: 'shoes_evening_all', item_type: 'shoes', name: 'Evening Oxfords (Waterproof)', color: 'black', material: 'treated_leather', size: '42', style: ['evening','formal'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['evening'], is_clean: true, metadata: {} },

    // Beach core
    { item_id: 'top_beach_all', item_type: 'top', name: 'All-Weather Beach Shirt', color: 'white', material: 'quick_dry', size: 'M', style: ['beach','casual'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['beach'], is_clean: true, metadata: {} },
    { item_id: 'bottom_beach_all', item_type: 'bottom', name: 'Hybrid Swim Shorts', color: 'navy', material: 'quick_dry', size: 'M', style: ['beach','casual'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['beach'], is_clean: true, metadata: {} },
    { item_id: 'shoes_beach_all', item_type: 'shoes', name: 'Water Sandals', color: 'black', material: 'rubber', size: '42', style: ['beach','casual'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['beach'], is_clean: true, metadata: {} },

    // Party core
    { item_id: 'top_party_all', item_type: 'top', name: 'All-Weather Party Shirt', color: 'burgundy', material: 'performance_blend', size: 'M', style: ['party','classic'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['party'], is_clean: true, metadata: {} },
    { item_id: 'bottom_party_all', item_type: 'bottom', name: 'Party Trousers', color: 'black', material: 'tech_wool', size: '32', style: ['party','classic'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['party'], is_clean: true, metadata: {} },
    { item_id: 'shoes_party_all', item_type: 'shoes', name: 'Party Loafers (Weatherproof)', color: 'black', material: 'treated_leather', size: '42', style: ['party','classic'], weather_suitability: ['cool','mild','warm','hot','cold','rainy'], occasion_suitability: ['party'], is_clean: true, metadata: {} }
  ];
  inventoryEl.value = JSON.stringify(defaultInventory, null, 2);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    resultsEl.innerHTML = '';

    const occasion_type = document.getElementById('occasion_type').value;
    const weather = document.getElementById('weather').value;
    const max_outfits = parseInt(document.getElementById('max_outfits').value, 10) || 2;
    const consider_previous = document.getElementById('consider_previous').checked;

    let inventory;
    try {
      inventory = JSON.parse(inventoryEl.value);
      if (!Array.isArray(inventory)) throw new Error('Inventory must be an array');
    } catch (err) {
      resultsEl.innerHTML = `<div class="error">Invalid inventory JSON: ${err.message}</div>`;
      return;
    }

    const payload = {
      user_info: {
        user_id: 'demo-user',
        body_type: 'rectangle',
        skin_tone: 'medium',
        height_cm: 170,
        style_preferences: ['casual', 'minimalist'],
        color_preferences: ['blue', 'white', 'black'],
        fit_preferences: {}
      },
      occasion: {
        occasion_type,
        weather,
        time_of_day: 'afternoon',
        location: 'office',
        dress_code: occasion_type,
        additional_notes: null
      },
      inventory,
      max_outfits,
      consider_previous_outfits: consider_previous
    };

    // Simple loader
    const loading = document.createElement('div');
    loading.className = 'loading';
    loading.textContent = 'Generating recommendations...';
    resultsEl.appendChild(loading);

    try {
      const res = await fetch('/api/v1/recommend-outfits', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      resultsEl.removeChild(loading);

      if (!res.ok) {
        const errText = await res.text();
        resultsEl.innerHTML = `<div class="error">Request failed: ${res.status} - ${errText}</div>`;
        return;
      }

      const outfits = await res.json();
      if (!outfits || outfits.length === 0) {
        resultsEl.innerHTML = '<div class="empty">No outfits found. Try adjusting inputs or inventory.</div>';
        return;
      }

      outfits.forEach((outfit, i) => {
        const card = document.createElement('div');
        card.className = 'outfit-card';
        const scorePct = (typeof outfit.confidence_score === 'number') 
          ? Math.round(outfit.confidence_score * 100) 
          : null;
        const score = (scorePct !== null) ? `${scorePct}%` : '—';

        const itemsList = (outfit.items || [])
          .map(it => `<li><strong>${it.name || it.item_id}</strong> <span class="muted">(${it.item_type})</span></li>`) 
          .join('');

        card.innerHTML = `
          <h3>Outfit #${i + 1} <span class="badge">${score}</span></h3>
          <ul>${itemsList}</ul>
        `;
        resultsEl.appendChild(card);
      });
    } catch (err) {
      resultsEl.innerHTML = `<div class="error">Unexpected error: ${err.message}</div>`;
    }
  });
});
