import { useState, useEffect } from 'react';
import { getTranslation } from '../translations';

const RiceDiseasesInfo = ({ language = 'en' }) => {
  const [selectedDisease, setSelectedDisease] = useState('rice-blast');
  const [selectedCrop, setSelectedCrop] = useState('rice');
  const [searchTerm, setSearchTerm] = useState('');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  const [severityLevel, setSeverityLevel] = useState(3);
  const [showCalculator, setShowCalculator] = useState(false);
  const [treatmentCost, setTreatmentCost] = useState(0);
  const [fieldSize, setFieldSize] = useState(1);
  const [showImageModal, setShowImageModal] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [favorites, setFavorites] = useState([]);

  // Function to get first disease of a crop
  const getFirstDiseaseOfCrop = (crop) => {
    const cropDiseases = Object.entries(diseases).filter(([, disease]) => disease.crop === crop);
    return cropDiseases.length > 0 ? cropDiseases[0][0] : null;
  };

  // Handle crop selection with automatic disease selection
  const handleCropSelection = (crop) => {
    setSelectedCrop(crop);
    const firstDisease = getFirstDiseaseOfCrop(crop);
    if (firstDisease) {
      setSelectedDisease(firstDisease);
    }
  };

  // Toggle favorite diseases
  const toggleFavorite = (diseaseKey) => {
    setFavorites(prev =>
      prev.includes(diseaseKey)
        ? prev.filter(fav => fav !== diseaseKey)
        : [...prev, diseaseKey]
    );
  };

  // Calculate treatment cost
  const calculateCost = () => {
    const disease = diseases[selectedDisease];
    if (!disease) return;

    const baseCost = disease.treatmentCost || 500;
    const severityMultiplier = severityLevel / 3;
    const areaMultiplier = fieldSize;
    const totalCost = baseCost * severityMultiplier * areaMultiplier;

    setTreatmentCost(Math.round(totalCost));
  };

  // Get severity color
  const getSeverityColor = (level) => {
    switch (level) {
      case 1: return 'text-green-600 bg-green-100';
      case 2: return 'text-yellow-600 bg-yellow-100';
      case 3: return 'text-orange-600 bg-orange-100';
      case 4: return 'text-red-600 bg-red-100';
      case 5: return 'text-red-800 bg-red-200';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  // Get severity label
  const getSeverityLabel = (level) => {
    switch (level) {
      case 1: return 'Low';
      case 2: return 'Mild';
      case 3: return 'Moderate';
      case 4: return 'Severe';
      case 5: return 'Critical';
      default: return 'Unknown';
    }
  };
  const [translatedContent, setTranslatedContent] = useState({});
  const [isTranslating, setIsTranslating] = useState(false);

  // Backend translation API integration
  const translateText = async (text, targetLang) => {
    if (targetLang === 'en') return text;

    try {
      const response = await fetch('http://localhost:8000/api/translate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          target_lang: targetLang
        })
      });

      const data = await response.json();
      return data.translated_text || text;
    } catch (error) {
      console.error('Translation error:', error);
      return text; // Return original text if translation fails
    }
  };

  const translateDiseaseContent = async (disease, targetLang) => {
    if (targetLang === 'en') return disease;

    const translated = { ...disease };

    // Translate name
    translated.name = await translateText(disease.name, targetLang);

    // Translate symptoms
    translated.symptoms = await Promise.all(
      disease.symptoms.map(symptom => translateText(symptom, targetLang))
    );

    // Translate causes
    translated.causes = await translateText(disease.causes, targetLang);

    // Translate management strategies
    translated.management = await Promise.all(
      disease.management.map(strategy => translateText(strategy, targetLang))
    );

    // Translate prevention measures
    translated.prevention = await Promise.all(
      disease.prevention.map(measure => translateText(measure, targetLang))
    );

    return translated;
  };

  useEffect(() => {
    const loadTranslations = async () => {
      if (language === 'en') {
        setTranslatedContent({});
        return;
      }

      setIsTranslating(true);
      try {
        const translatedDisease = await translateDiseaseContent(diseases[selectedDisease], language);
        setTranslatedContent({ [selectedDisease]: translatedDisease });
      } catch (error) {
        console.error('Translation loading error:', error);
        // Fallback to original content if translation fails
        setTranslatedContent({ [selectedDisease]: diseases[selectedDisease] });
      } finally {
        setIsTranslating(false);
      }
    };

    // Add a small delay to avoid too many API calls
    const timeoutId = setTimeout(loadTranslations, 500);
    return () => clearTimeout(timeoutId);
  }, [language, selectedDisease]);

  const crops = {
    rice: 'Rice',
    wheat: 'Wheat',
    maize: 'Maize/Corn',
    tomato: 'Tomato',
    potato: 'Potato',
    cotton: 'Cotton',
    soybean: 'Soybean',
    sugarcane: 'Sugarcane'
  };

  const diseases = {
    // Rice Diseases
    'rice-blast': {
      crop: 'rice',
      name: 'Rice Blast',
      scientificName: 'Magnaporthe oryzae',
      severity: 4,
      economicImpact: 'Up to 30% yield loss in severe cases',
      treatmentCost: 450,
      regionalInfo: 'Most prevalent in South and Southeast Asia, especially during wet season',
      images: ['/static/images/crops/rice-blast-1.jpg', '/static/images/crops/rice-blast-2.jpg'],
      symptoms: [
        'Diamond-shaped lesions with gray centers and brown borders on leaves',
        'Lesions can coalesce to form large necrotic areas',
        'Neck blast affects the panicle neck causing blanking',
        'Node blast affects stem nodes',
        'Panicle blast causes rotten neck and empty grains'
      ],
      causes: 'Fungus Magnaporthe oryzae, thrives in warm, humid conditions (25-30°C) with high nitrogen fertilization, poor drainage, and dense planting',
      lifeCycle: 'Fungus survives in infected seeds, crop residues, and soil. Spores spread by wind and water splash.',
      favorableConditions: 'Temperature: 25-30°C, Humidity: >90%, Leaf wetness: >8 hours',
      management: [
        'Use resistant varieties (e.g., IR64, IR36, CO-43)',
        'Avoid excessive nitrogen fertilization (>120 kg/ha)',
        'Maintain proper plant spacing (20x15 cm)',
        'Apply systemic fungicides like tricyclazole (75% WP @ 0.6g/L)',
        'Practice crop rotation with legumes or vegetables',
        'Implement proper water management to avoid prolonged leaf wetness'
      ],
      prevention: [
        'Use certified disease-free seeds treated with fungicides',
        'Avoid planting during high disease pressure periods',
        'Implement proper field sanitation - remove crop residues',
        'Use balanced fertilization with recommended NPK ratios',
        'Practice integrated nutrient management',
        'Monitor fields regularly and apply fungicides preventively'
      ],
      biologicalControl: [
        'Use Trichoderma spp. as seed treatment',
        'Apply Pseudomonas fluorescens for soil application',
        'Introduce natural enemies of fungal pathogens'
      ],
      chemicalControl: [
        'Tricyclazole 75% WP @ 0.6g/L (2-3 applications)',
        'Edifenphos 50% EC @ 1.0ml/L',
        'Isoprothiolane 40% EC @ 1.0ml/L',
        'Kasugamycin 3% SL @ 2.0ml/L (for bacterial blight complex)'
      ],
      expertTips: [
        'Apply first fungicide spray at panicle initiation stage',
        'Use weather-based disease forecasting systems',
        'Maintain field sanitation by removing infected plants immediately',
        'Avoid working in fields when plants are wet'
      ]
    },
    'rice-bacterial-blight': {
      crop: 'rice',
      name: 'Rice Bacterial Blight',
      scientificName: 'Xanthomonas oryzae pv. oryzae',
      severity: 5,
      economicImpact: 'Up to 50% yield loss in epidemic conditions',
      treatmentCost: 600,
      regionalInfo: 'Common in irrigated rice ecosystems, especially in tropical regions',
      images: ['/static/images/crops/rice-blight-1.jpg', '/static/images/crops/rice-blight-2.jpg'],
      symptoms: [
        'Water-soaked lesions that turn yellow then brown',
        'Lesions start at leaf tips and margins, spread along veins',
        'Leaves may wilt and die in severe cases',
        'Creamy bacterial ooze visible in early morning',
        'Lesions can be up to 30cm long in severe infections',
        'Yellow halos around lesions in early stages'
      ],
      causes: 'Bacterium Xanthomonas oryzae pv. oryzae, spreads through infected seeds, contaminated irrigation water, and wind-driven rain. Survives in seeds for up to 2 years.',
      lifeCycle: 'Bacteria enter through wounds or natural openings. Multiplies rapidly in vascular tissues, spreads through xylem vessels.',
      favorableConditions: 'Temperature: 25-30°C, Humidity: >70%, Rain: Frequent, Wounds: From insects or mechanical damage',
      management: [
        'Use resistant varieties (e.g., IRBB series, improved lines)',
        'Treat seeds with hot water (52°C for 30 minutes) or antibiotics',
        'Avoid overhead irrigation - use furrow or drip irrigation',
        'Apply copper-based bactericides (Copper oxychloride 50% WP @ 3g/L)',
        'Remove and destroy infected plant debris immediately',
        'Implement strict quarantine measures for infected fields'
      ],
      prevention: [
        'Use certified seeds from reliable sources',
        'Implement 2-3 year crop rotation with non-host crops',
        'Avoid working in fields when plants are wet',
        'Maintain proper drainage to prevent water stagnation',
        'Control insect vectors that create entry wounds',
        'Practice field sanitation and weed control'
      ],
      biologicalControl: [
        'Use antagonistic bacteria like Pseudomonas spp.',
        'Apply bio-control agents containing Bacillus subtilis',
        'Introduce beneficial microbes through seed treatment'
      ],
      chemicalControl: [
        'Streptomycin sulfate 90% SP @ 1g/L (seed treatment)',
        'Copper oxychloride 50% WP @ 3g/L (foliar spray)',
        'Kasugamycin 3% SL @ 2ml/L (for severe infections)',
        'Plantomycin 10% WP @ 1g/L (systemic antibiotic)'
      ],
      expertTips: [
        'Monitor fields daily during tillering and panicle initiation',
        'Apply first spray at first symptom appearance',
        'Use resistant varieties as primary control method',
        'Avoid nitrogen fertilization during disease development'
      ]
    },

    // Wheat Diseases
    'wheat-rust': {
      crop: 'wheat',
      name: 'Wheat Rust',
      scientificName: 'Puccinia spp.',
      symptoms: [
        'Orange to reddish-brown pustules on leaves and stems',
        'Pustules contain powdery spores',
        'Yellowing and premature leaf death',
        'Reduced grain filling and yield loss'
      ],
      causes: 'Fungi Puccinia graminis (stem rust), P. triticina (leaf rust), P. striiformis (stripe rust)',
      management: [
        'Use resistant varieties',
        'Apply fungicides at early disease detection',
        'Practice crop rotation',
        'Remove volunteer wheat plants',
        'Use balanced nitrogen fertilization'
      ],
      prevention: [
        'Plant resistant cultivars',
        'Monitor fields regularly',
        'Avoid late planting',
        'Implement proper field sanitation'
      ]
    },

    // Tomato Diseases
    'tomato-late-blight': {
      crop: 'tomato',
      name: 'Tomato Late Blight',
      scientificName: 'Phytophthora infestans',
      symptoms: [
        'Dark, water-soaked lesions on leaves',
        'White fungal growth on leaf undersides',
        'Rapid spreading during humid conditions',
        'Fruit rot with firm, dark lesions'
      ],
      causes: 'Oomycete Phytophthora infestans, thrives in cool, wet conditions',
      management: [
        'Apply fungicides preventively',
        'Improve air circulation',
        'Avoid overhead irrigation',
        'Remove infected plant parts immediately',
        'Use resistant varieties when available'
      ],
      prevention: [
        'Plant in well-drained soil',
        'Space plants properly for air circulation',
        'Avoid working with wet plants',
        'Rotate crops annually'
      ]
    },

    // Potato Diseases
    'potato-late-blight': {
      crop: 'potato',
      name: 'Potato Late Blight',
      scientificName: 'Phytophthora infestans',
      symptoms: [
        'Dark, water-soaked spots on leaves',
        'White fungal growth on leaf undersides',
        'Rapid blighting of foliage',
        'Tubers develop firm, dark rot'
      ],
      causes: 'Oomycete Phytophthora infestans, favors cool, moist conditions',
      management: [
        'Apply fungicides regularly during wet periods',
        'Remove infected plants immediately',
        'Improve drainage in fields',
        'Store tubers in cool, dry conditions',
        'Use resistant varieties'
      ],
      prevention: [
        'Plant certified disease-free seed potatoes',
        'Avoid overhead irrigation',
        'Ensure proper plant spacing',
        'Implement crop rotation'
      ]
    },

    // Maize/Corn Diseases
    'maize-rust': {
      crop: 'maize',
      name: 'Maize Rust',
      scientificName: 'Puccinia sorghi',
      symptoms: [
        'Small, circular to elongated pustules',
        'Orange to reddish-brown spores',
        'Pustules appear on both leaf surfaces',
        'Severe infections cause leaf yellowing'
      ],
      causes: 'Fungus Puccinia sorghi, spreads through wind-borne spores',
      management: [
        'Apply fungicides when disease appears',
        'Use resistant hybrids',
        'Practice crop rotation',
        'Remove volunteer corn plants',
        'Monitor fields regularly'
      ],
      prevention: [
        'Plant resistant varieties',
        'Avoid late planting',
        'Implement proper field sanitation',
        'Use balanced fertilization'
      ]
    },

    // Cotton Diseases
    'cotton-bacterial-blight': {
      crop: 'cotton',
      name: 'Cotton Bacterial Blight',
      scientificName: 'Xanthomonas citri pv. malvacearum',
      symptoms: [
        'Angular leaf spots with yellow halos',
        'Dark, sunken lesions on bolls',
        'Premature defoliation',
        'Reduced fiber quality and yield'
      ],
      causes: 'Bacterium Xanthomonas citri pv. malvacearum, spreads through infected seeds and plant debris',
      management: [
        'Use disease-free seeds',
        'Apply copper-based bactericides',
        'Practice crop rotation',
        'Remove infected plant debris',
        'Use resistant varieties'
      ],
      prevention: [
        'Use certified seeds',
        'Implement proper field sanitation',
        'Avoid wet foliage operations',
        'Practice long crop rotations'
      ]
    },

    // Soybean Diseases
    'soybean-rust': {
      crop: 'soybean',
      name: 'Soybean Rust',
      scientificName: 'Phakopsora pachyrhizi',
      symptoms: [
        'Small, reddish-brown pustules on leaves',
        'Yellow spots (chlorosis) around pustules',
        'Premature defoliation',
        'Reduced pod development and yield'
      ],
      causes: 'Fungus Phakopsora pachyrhizi, spreads through wind-borne spores',
      management: [
        'Apply fungicides preventively',
        'Use resistant varieties',
        'Monitor fields regularly',
        'Practice crop rotation',
        'Remove volunteer soybeans'
      ],
      prevention: [
        'Plant resistant cultivars',
        'Implement proper field sanitation',
        'Avoid late planting',
        'Use fungicide seed treatments'
      ]
    },

    // Sugarcane Diseases
    'sugarcane-rust': {
      crop: 'sugarcane',
      name: 'Sugarcane Rust',
      scientificName: 'Puccinia melanocephala',
      symptoms: [
        'Reddish-brown elongated pustules on leaves',
        'Pustules arranged in rows parallel to leaf veins',
        'Yellowing and drying of leaves',
        'Reduced sugar content and yield'
      ],
      causes: 'Fungus Puccinia melanocephala, thrives in warm, humid conditions',
      management: [
        'Use resistant varieties',
        'Apply fungicides when disease appears',
        'Improve field drainage',
        'Practice proper irrigation',
        'Remove infected leaves'
      ],
      prevention: [
        'Plant resistant sugarcane varieties',
        'Implement crop rotation',
        'Maintain proper plant spacing',
        'Monitor humidity levels'
      ]
    }
  };

  const currentDisease = translatedContent[selectedDisease] || diseases[selectedDisease];

  return (
    <div className="max-w-6xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-blue-600 text-white p-6">
        <h1 className="text-3xl font-bold mb-2">{getTranslation('plantDiseasesInfo', language)}</h1>
        <p className="text-green-100">{getTranslation('comprehensiveGuide', language)}</p>
      </div>

      <div className="flex flex-col lg:flex-row">
        {/* Enhanced Sidebar */}
        <div className={`bg-gradient-to-b from-green-50 to-blue-50 border-r border-gray-200 shadow-lg transition-all duration-300 ${
          sidebarCollapsed ? 'lg:w-16' : 'lg:w-1/4'
        }`}>
          {!sidebarCollapsed && (
            <div className="p-6">
            {/* Header with Toggle */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                {!sidebarCollapsed && (
                  <h2 className="text-xl font-bold text-gray-800">🌾 {getTranslation('cropDiseases', language)}</h2>
                )}
                <button
                  onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
                  className="p-2 rounded-lg hover:bg-white/50 transition-colors duration-200"
                >
                  {sidebarCollapsed ? '→' : '←'}
                </button>
              </div>
              {!sidebarCollapsed && (
                <p className="text-sm text-gray-600">{getTranslation('selectCrop', language)}</p>
              )}
            </div>

            {/* Search Bar */}
            {!sidebarCollapsed && (
              <div className="mb-6">
                <div className="relative">
                  <input
                    type="text"
                    placeholder={getTranslation('searchProducts', language)}
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span className="text-gray-400">🔍</span>
                  </div>
                </div>
              </div>
            )}

          {/* Quick Stats */}
          <div className="bg-white rounded-lg p-4 mb-6 shadow-sm">
            <h3 className="font-semibold text-gray-800 mb-3 flex items-center">
              <span className="mr-2">📊</span>
              {getTranslation('statistics', language)}
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">{getTranslation('totalCrops', language)}:</span>
                <span className="font-medium text-green-600">{Object.keys(crops).length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">{getTranslation('totalDiseases', language)}:</span>
                <span className="font-medium text-blue-600">{Object.keys(diseases).length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">{getTranslation('aiAccuracy', language)}:</span>
                <span className="font-medium text-purple-600">95%</span>
              </div>
            </div>
          </div>

          {/* Crop Selection */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
              <span className="mr-2">🌱</span>
              {getTranslation('selectCrop', language)}
            </h3>
            <div className="space-y-2">
              {Object.entries(crops).map(([key, cropName]) => (
                <button
                  key={key}
                  onClick={() => handleCropSelection(key)}
                  className={`w-full text-left p-3 rounded-lg transition-all duration-200 transform hover:scale-105 ${
                    selectedCrop === key
                      ? 'bg-green-600 text-white shadow-md'
                      : 'bg-white text-gray-700 hover:bg-green-50 hover:shadow-sm'
                  }`}
                >
                  <div className="flex items-center">
                    <span className="mr-3 text-lg">
                      {key === 'rice' && '🌾'}
                      {key === 'wheat' && '🌿'}
                      {key === 'maize' && '🌽'}
                      {key === 'tomato' && '🍅'}
                      {key === 'potato' && '🥔'}
                      {key === 'cotton' && '🌸'}
                      {key === 'soybean' && '🫘'}
                      {key === 'sugarcane' && '🎋'}
                    </span>
                    <div>
                      <div className="font-medium">{cropName}</div>
                      <div className="text-xs opacity-75">
                        {Object.values(diseases).filter(d => d.crop === key).length} {getTranslation('totalDiseases', language).toLowerCase()}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Disease Selection for selected crop */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
              <span className="mr-2">🔬</span>
              {getTranslation('diseasesFor', language)} {crops[selectedCrop]}
            </h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {(() => {
                const filteredDiseases = Object.entries(diseases)
                  .filter(([, disease]) => disease.crop === selectedCrop);

                if (filteredDiseases.length === 0) {
                  return (
                    <div className="text-center py-8 text-gray-500 bg-white rounded-lg p-4">
                      <div className="text-2xl mb-2">📝</div>
                      <p className="text-sm">{getTranslation('noPrediction', language)}</p>
                      <p className="text-xs mt-1">Disease data will be added soon.</p>
                    </div>
                  );
                }

                return filteredDiseases.map(([key, disease]) => (
                  <button
                    key={key}
                    onClick={() => setSelectedDisease(key)}
                    className={`w-full text-left p-3 rounded-lg transition-all duration-200 ${
                      selectedDisease === key
                        ? 'bg-blue-600 text-white shadow-md transform scale-105'
                        : 'bg-white text-gray-700 hover:bg-blue-50 hover:shadow-sm'
                    }`}
                  >
                    <div className="font-medium text-sm">{disease.name}</div>
                    <div className="text-xs opacity-75 italic mt-1">{disease.scientificName}</div>
                  </button>
                ));
              })()}
            </div>
          </div>

          {/* Navigation Tips */}
          <div className="bg-blue-50 rounded-lg p-4">
            <h4 className="font-semibold text-blue-800 mb-2 flex items-center">
              <span className="mr-2">💡</span>
              {getTranslation('tips', language)}
            </h4>
            <ul className="text-xs text-blue-700 space-y-1">
              <li>• {getTranslation('clickCrops', language)}</li>
              <li>• {getTranslation('useLanguageSelector', language)}</li>
              <li>• {getTranslation('researchBased', language)}</li>
              <li>• {getTranslation('monitoringPreventsLoss', language)}</li>
            </ul>
          </div>
          </div>
        )}
      </div>

        {/* Enhanced Disease Details */}
        <div className="lg:w-3/4 p-6">
          {isTranslating && language !== 'en' && (
            <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center space-x-2 text-blue-700">
                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Translating content to {language.toUpperCase()}...</span>
              </div>
            </div>
          )}

          {/* Disease Header with Actions */}
          <div className="mb-6 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-6 border border-green-200">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2">{currentDisease.name}</h2>
                <p className="text-lg text-green-600 italic mb-2">{currentDisease.scientificName}</p>
                <div className="flex items-center space-x-4">
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getSeverityColor(currentDisease.severity)}`}>
                    Severity: {getSeverityLabel(currentDisease.severity)}
                  </span>
                  <span className="text-sm text-gray-600">💰 Est. Treatment Cost: ₹{currentDisease.treatmentCost}/acre</span>
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => toggleFavorite(selectedDisease)}
                  className={`p-2 rounded-lg transition-colors ${
                    favorites.includes(selectedDisease)
                      ? 'bg-red-100 text-red-600 hover:bg-red-200'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {favorites.includes(selectedDisease) ? '❤️' : '🤍'}
                </button>
                <button
                  onClick={() => setShowCalculator(!showCalculator)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  🧮 {getTranslation('treatmentCostCalculator', language)}
                </button>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg p-3 text-center">
                <div className="text-lg font-bold text-red-600">{currentDisease.economicImpact}</div>
                <div className="text-xs text-gray-600">Economic Impact</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center">
                <div className="text-lg font-bold text-blue-600">{currentDisease.regionalInfo}</div>
                <div className="text-xs text-gray-600">Regional Prevalence</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center">
                <div className="text-lg font-bold text-green-600">{currentDisease.favorableConditions}</div>
                <div className="text-xs text-gray-600">Favorable Conditions</div>
              </div>
            </div>
          </div>

          {/* Cost Calculator Modal */}
          {showCalculator && (
            <div className="mb-6 bg-white rounded-xl shadow-lg p-6 border border-blue-200">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">🧮</span>
                Treatment Cost Calculator
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Disease Severity</label>
                  <select
                    value={severityLevel}
                    onChange={(e) => setSeverityLevel(parseInt(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value={1}>Low (1x cost)</option>
                    <option value={2}>Mild (1.3x cost)</option>
                    <option value={3}>Moderate (1.7x cost)</option>
                    <option value={4}>Severe (2.2x cost)</option>
                    <option value={5}>Critical (3x cost)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Field Size (acres)</label>
                  <input
                    type="number"
                    value={fieldSize}
                    onChange={(e) => setFieldSize(Math.max(0.1, parseFloat(e.target.value) || 1))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    min="0.1"
                    step="0.1"
                  />
                </div>
                <div className="flex items-end">
                  <button
                    onClick={calculateCost}
                    className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    Calculate Cost
                  </button>
                </div>
              </div>
              {treatmentCost > 0 && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">₹{treatmentCost.toLocaleString()}</div>
                    <div className="text-sm text-green-700">Estimated Total Treatment Cost</div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Tab Navigation */}
          <div className="mb-6">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                {[
                  { key: 'overview', label: getTranslation('overview', language) },
                  { key: 'symptoms', label: getTranslation('symptoms', language) },
                  { key: 'causes', label: getTranslation('causes', language) },
                  { key: 'management', label: getTranslation('management', language) },
                  { key: 'prevention', label: getTranslation('prevention', language) },
                  { key: 'images', label: 'Images' }
                ].map((tab) => (
                  <button
                    key={tab.key}
                    onClick={() => setActiveTab(tab.key)}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === tab.key
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Tab Content */}
          <div className="space-y-6">
            {activeTab === 'overview' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white rounded-xl shadow-md p-6">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                    <span className="mr-2">📊</span>
                    {getTranslation('diseaseOverview', language)}
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Scientific Name:</span>
                      <span className="font-medium">{currentDisease.scientificName}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Severity Level:</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(currentDisease.severity)}`}>
                        {getSeverityLabel(currentDisease.severity)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Economic Impact:</span>
                      <span className="font-medium text-red-600">{currentDisease.economicImpact}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Regional Info:</span>
                      <span className="font-medium text-blue-600">{currentDisease.regionalInfo}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-xl shadow-md p-6">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                    <span className="mr-2">🔄</span>
                    {getTranslation('diseaseLifeCycle', language)}
                  </h3>
                  <p className="text-gray-700 leading-relaxed">{currentDisease.lifeCycle}</p>
                </div>
              </div>
            )}

            {activeTab === 'symptoms' && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <span className="mr-2">🔍</span>
                  Symptoms & Identification
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {currentDisease.symptoms.map((symptom, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                      <span className="flex-shrink-0 w-6 h-6 bg-red-100 text-red-600 rounded-full flex items-center justify-center text-sm font-bold">
                        {index + 1}
                      </span>
                      <p className="text-gray-700 leading-relaxed">{symptom}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'causes' && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <span className="mr-2">🦠</span>
                  Causal Agent & Conditions
                </h3>
                <div className="space-y-4">
                  <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                    <h4 className="font-semibold text-red-800 mb-2">Primary Cause</h4>
                    <p className="text-red-700">{currentDisease.causes}</p>
                  </div>
                  <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <h4 className="font-semibold text-yellow-800 mb-2">Favorable Conditions</h4>
                    <p className="text-yellow-700">{currentDisease.favorableConditions}</p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'management' && (
              <div className="space-y-6">
                <div className="bg-white rounded-xl shadow-md p-6">
                  <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                    <span className="mr-2">💊</span>
                    Management Strategies
                  </h3>
                  <div className="space-y-3">
                    {currentDisease.management.map((strategy, index) => (
                      <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                        <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-bold">
                          {index + 1}
                        </span>
                        <p className="text-blue-700 leading-relaxed">{strategy}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {currentDisease.biologicalControl && (
                  <div className="bg-white rounded-xl shadow-md p-6">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                      <span className="mr-2">🌱</span>
                      Biological Control Methods
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {currentDisease.biologicalControl.map((method, index) => (
                        <div key={index} className="p-3 bg-green-50 border border-green-200 rounded-lg">
                          <p className="text-green-700 text-sm">{method}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {currentDisease.chemicalControl && (
                  <div className="bg-white rounded-xl shadow-md p-6">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                      <span className="mr-2">🧪</span>
                      Chemical Control Options
                    </h3>
                    <div className="space-y-2">
                      {currentDisease.chemicalControl.map((chemical, index) => (
                        <div key={index} className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
                          <p className="text-purple-700 text-sm font-medium">{chemical}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'prevention' && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <span className="mr-2">🛡️</span>
                  Prevention Measures
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {currentDisease.prevention.map((measure, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-green-50 rounded-lg">
                      <span className="flex-shrink-0 w-6 h-6 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-sm font-bold">
                        {index + 1}
                      </span>
                      <p className="text-green-700 leading-relaxed">{measure}</p>
                    </div>
                  ))}
                </div>

                {currentDisease.expertTips && (
                  <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <h4 className="font-semibold text-blue-800 mb-3 flex items-center">
                      <span className="mr-2">👨‍🌾</span>
                      Expert Tips
                    </h4>
                    <ul className="space-y-2">
                      {currentDisease.expertTips.map((tip, index) => (
                        <li key={index} className="text-blue-700 text-sm flex items-start">
                          <span className="mr-2">•</span>
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'images' && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <span className="mr-2">📸</span>
                  Disease Images & Visual Guide
                </h3>
                {currentDisease.images && currentDisease.images.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {currentDisease.images.map((image, index) => (
                      <div key={index} className="relative group cursor-pointer" onClick={() => {
                        setSelectedImage(image);
                        setShowImageModal(true);
                      }}>
                        <img
                          src={image}
                          alt={`${currentDisease.name} symptom ${index + 1}`}
                          className="w-full h-48 object-cover rounded-lg shadow-md group-hover:shadow-lg transition-shadow"
                        />
                        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity rounded-lg flex items-center justify-center">
                          <span className="text-white opacity-0 group-hover:opacity-100 transition-opacity">
                            Click to enlarge
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12 text-gray-500">
                    <div className="text-4xl mb-4">📷</div>
                    <p className="text-lg">No images available for this disease</p>
                    <p className="text-sm mt-2">Images will be added soon for better visual identification</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Enhanced Additional Information */}
          <div className="mt-6 bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 rounded-xl p-6">
            <h4 className="font-bold text-blue-800 mb-4 flex items-center text-lg">
              <span className="mr-2">💡</span>
              Integrated Disease Management (IDM) Guidelines
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-sm font-bold">1</span>
                  <div>
                    <h5 className="font-semibold text-green-800">Early Detection</h5>
                    <p className="text-sm text-green-700">Monitor fields regularly and identify symptoms early</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-bold">2</span>
                  <div>
                    <h5 className="font-semibold text-blue-800">Integrated Approach</h5>
                    <p className="text-sm text-blue-700">Combine cultural, biological, and chemical methods</p>
                  </div>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-sm font-bold">3</span>
                  <div>
                    <h5 className="font-semibold text-purple-800">Local Expertise</h5>
                    <p className="text-sm text-purple-700">Consult agricultural extension services</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-8 h-8 bg-orange-100 text-orange-600 rounded-full flex items-center justify-center text-sm font-bold">4</span>
                  <div>
                    <h5 className="font-semibold text-orange-800">Regular Monitoring</h5>
                    <p className="text-sm text-orange-700">Continuous field surveillance for timely intervention</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Image Modal */}
      {showImageModal && selectedImage && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="max-w-4xl w-full max-h-[90vh]">
            <div className="bg-white rounded-xl overflow-hidden">
              <div className="flex justify-between items-center p-4 border-b">
                <h3 className="text-lg font-semibold text-gray-800">{currentDisease.name} - Symptom Image</h3>
                <button
                  onClick={() => setShowImageModal(false)}
                  className="text-gray-400 hover:text-gray-600 p-2"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="p-4">
                <img
                  src={selectedImage}
                  alt={`${currentDisease.name} symptom`}
                  className="w-full h-auto max-h-[70vh] object-contain rounded-lg"
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-600">
            Comprehensive plant diseases information and management guide
          </div>
          <div className="text-sm text-gray-500">
            Last updated: September 2025
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiceDiseasesInfo;