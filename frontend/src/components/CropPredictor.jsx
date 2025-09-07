import { useState } from 'react';
import { predictDisease } from '../apiService';
import { getTranslation } from '../translations';

const CropPredictor = ({ language = 'en' }) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [treatments, setTreatments] = useState([]);
  const [preventions, setPreventions] = useState([]);
  const [diseaseImage, setDiseaseImage] = useState('');

  const handleReset = () => {
    setSelectedImage(null);
    setPrediction('');
    setError('');
    setTreatments([]);
    setPreventions([]);
    setDiseaseImage('');
  };

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPrediction('');
      setError('');
    }
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      setError(getTranslation('noImageSelected', language));
      return;
    }

    setLoading(true);
    setError('');
    try {
      const result = await predictDisease(selectedImage);
      setPrediction(result.result || getTranslation('noPrediction', language));
      setTreatments(result.treatments || []);
      setPreventions(result.preventions || []);
      setDiseaseImage(result.disease_info?.image_path || '');
    } catch (err) {
      console.error('Prediction error:', err);
      setError(getTranslation('failedToPredict', language));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden">
      <div className="p-6">
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-gray-900">{getTranslation('title', language)}</h2>
          <p className="text-sm text-gray-600 mt-1">
            {getTranslation('subtitle', language)}
          </p>
        </div>

        <div className="mb-4">
          <label htmlFor="image-upload" className="block text-sm font-medium text-gray-700 mb-2">
            {getTranslation('uploadImage', language)}
          </label>
          <input
            id="image-upload"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        {selectedImage && (
          <div className="mb-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">{getTranslation('uploadedImage', language) || 'Uploaded Image'}</h4>
                <img
                  src={URL.createObjectURL(selectedImage)}
                  alt="Selected"
                  className="w-full h-48 object-cover rounded-lg border-2 border-gray-200"
                />
              </div>
              {diseaseImage && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">{getTranslation('diseaseReference', language) || 'Disease Reference'}</h4>
                  <img
                    src={`http://localhost:8000${diseaseImage}`}
                    alt="Disease reference"
                    className="w-full h-48 object-cover rounded-lg border-2 border-red-200"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                </div>
              )}
            </div>
          </div>
        )}

        <div className="flex space-x-2">
          <button
            onClick={handlePredict}
            disabled={loading || !selectedImage}
            className="flex-1 bg-blue-500 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded transition duration-200"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {getTranslation('predicting', language)}
              </div>
            ) : getTranslation('predictDisease', language)}
          </button>
          <button
            onClick={handleReset}
            className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded transition duration-200"
          >
            {getTranslation('reset', language)}
          </button>
        </div>

        {prediction && (
          <div className="mt-4 p-6 bg-gradient-to-r from-green-100 to-blue-100 border border-green-400 text-green-800 rounded-lg shadow-md">
            <div className="flex items-center space-x-3 mb-2">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">✓</span>
              </div>
              <div>
                <h3 className="text-lg font-bold">{getTranslation('prediction', language)}</h3>
                <p className="text-xl font-semibold text-green-700">{prediction}</p>
              </div>
            </div>
            {diseaseImage && (
              <div className="mt-4 p-3 bg-white/50 rounded-lg">
                <p className="text-sm text-gray-600">
                  📸 {getTranslation('referenceImageText', language)?.replace('{disease}', prediction) || `Reference image for ${prediction} is shown above for comparison`}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Solutions Section */}
        {treatments.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <span className="mr-2">🧪</span>
              {getTranslation('recommendedSolutions', language) || 'Recommended Solutions'}
            </h3>

            {/* Chemical/Insecticide Solutions */}
            {treatments.filter(t => t.treatment_type === 'chemical').length > 0 && (
              <div className="mb-6">
                <h4 className="text-md font-semibold text-red-700 mb-3 flex items-center">
                  <span className="mr-2">🧴</span>
                  {getTranslation('chemicalSolutions', language) || 'Chemical Solutions & Insecticides'}
                </h4>
                <div className="space-y-3">
                  {treatments.filter(t => t.treatment_type === 'chemical').map((treatment, index) => (
                    <div key={`chemical-${index}`} className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-3">
                        <h5 className="font-semibold text-red-900 text-lg">{treatment.name}</h5>
                        <div className="flex items-center">
                          <span className="text-sm text-gray-600 mr-2">Effectiveness:</span>
                          <div className="flex">
                            {[...Array(5)].map((_, i) => (
                              <span
                                key={i}
                                className={`text-sm ${i < treatment.effectiveness_rating ? 'text-yellow-500' : 'text-gray-300'}`}
                              >
                                ★
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      <p className="text-sm text-gray-700 mb-3 font-medium">{treatment.description}</p>

                      <div className="grid grid-cols-1 gap-2 text-sm">
                        <div className="bg-white rounded p-2">
                          <span className="font-semibold text-red-700">📍 Application:</span> {treatment.application_method}
                        </div>
                        {treatment.cost_estimate && (
                          <div className="bg-white rounded p-2">
                            <span className="font-semibold text-red-700">💰 Cost:</span> ${treatment.cost_estimate}
                          </div>
                        )}
                        {treatment.safety_precautions && (
                          <div className="bg-white rounded p-2">
                            <span className="font-semibold text-red-700">⚠️ Safety:</span> {treatment.safety_precautions}
                          </div>
                        )}
                        {treatment.duration_days && (
                          <div className="bg-white rounded p-2">
                            <span className="font-semibold text-red-700">⏱️ Duration:</span> {treatment.duration_days} days
                          </div>
                        )}
                      </div>

                      <div className="mt-3 flex items-center justify-between">
                        <span className="inline-block px-3 py-1 text-sm font-semibold rounded-full bg-red-100 text-red-800 border border-red-300">
                          🧪 Chemical/Insecticide
                        </span>
                        {treatment.regional_availability && (
                          <span className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
                            📍 {treatment.regional_availability}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Organic/Biological Solutions */}
            {treatments.filter(t => t.treatment_type === 'organic' || t.treatment_type === 'biological').length > 0 && (
              <div className="mb-6">
                <h4 className="text-md font-semibold text-green-700 mb-3 flex items-center">
                  <span className="mr-2">🌱</span>
                  {getTranslation('organicBiologicalSolutions', language) || 'Organic & Biological Solutions'}
                </h4>
                <div className="space-y-3">
                  {treatments.filter(t => t.treatment_type === 'organic' || t.treatment_type === 'biological').map((treatment, index) => (
                    <div key={`organic-${index}`} className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-3">
                        <h5 className="font-semibold text-green-900 text-lg">{treatment.name}</h5>
                        <div className="flex items-center">
                          <span className="text-sm text-gray-600 mr-2">Effectiveness:</span>
                          <div className="flex">
                            {[...Array(5)].map((_, i) => (
                              <span
                                key={i}
                                className={`text-sm ${i < treatment.effectiveness_rating ? 'text-yellow-500' : 'text-gray-300'}`}
                              >
                                ★
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      <p className="text-sm text-gray-700 mb-3 font-medium">{treatment.description}</p>

                      <div className="grid grid-cols-1 gap-2 text-sm">
                        <div className="bg-white rounded p-2">
                          <span className="font-semibold text-green-700">📍 Application:</span> {treatment.application_method}
                        </div>
                        {treatment.cost_estimate && (
                          <div className="bg-white rounded p-2">
                            <span className="font-semibold text-green-700">💰 Cost:</span> ${treatment.cost_estimate}
                          </div>
                        )}
                        {treatment.safety_precautions && (
                          <div className="bg-white rounded p-2">
                            <span className="font-semibold text-green-700">⚠️ Safety:</span> {treatment.safety_precautions}
                          </div>
                        )}
                        {treatment.duration_days && (
                          <div className="bg-white rounded p-2">
                            <span className="font-semibold text-green-700">⏱️ Duration:</span> {treatment.duration_days} days
                          </div>
                        )}
                      </div>

                      <div className="mt-3 flex items-center justify-between">
                        <span className={`inline-block px-3 py-1 text-sm font-semibold rounded-full ${
                          treatment.treatment_type === 'organic' ? 'bg-green-100 text-green-800 border border-green-300' :
                          'bg-purple-100 text-purple-800 border border-purple-300'
                        }`}>
                          {treatment.treatment_type === 'organic' ? '🌱 Organic' : '🦠 Biological'}
                        </span>
                        {treatment.regional_availability && (
                          <span className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
                            📍 {treatment.regional_availability}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* General Treatments */}
            {treatments.filter(t => !['chemical', 'organic', 'biological'].includes(t.treatment_type)).length > 0 && (
              <div className="mb-6">
                <h4 className="text-md font-semibold text-blue-700 mb-3 flex items-center">
                  <span className="mr-2">💊</span>
                  {getTranslation('generalTreatments', language) || 'General Treatments'}
                </h4>
                <div className="space-y-3">
                  {treatments.filter(t => !['chemical', 'organic', 'biological'].includes(t.treatment_type)).map((treatment, index) => (
                    <div key={`general-${index}`} className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h5 className="font-medium text-blue-900">{treatment.name}</h5>
                        <div className="flex items-center">
                          <span className="text-sm text-gray-600 mr-2">
                            {getTranslation('effectiveness', language)}:
                          </span>
                          <div className="flex">
                            {[...Array(5)].map((_, i) => (
                              <span
                                key={i}
                                className={`text-sm ${i < treatment.effectiveness_rating ? 'text-yellow-400' : 'text-gray-300'}`}
                              >
                                ★
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                      <p className="text-sm text-gray-700 mb-2">{treatment.description}</p>
                      <div className="text-xs text-gray-600 space-y-1">
                        <p><strong>{getTranslation('application', language)}:</strong> {treatment.application_method}</p>
                        {treatment.cost_estimate && (
                          <p><strong>{getTranslation('cost', language)}:</strong> ${treatment.cost_estimate}</p>
                        )}
                        {treatment.safety_precautions && (
                          <p><strong>{getTranslation('safety', language)}:</strong> {treatment.safety_precautions}</p>
                        )}
                      </div>
                      <div className="mt-2">
                        <span className="inline-block px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800">
                          {treatment.treatment_type || 'General'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Prevention Strategies Section */}
        {preventions.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <span className="mr-2">🛡️</span>
              {getTranslation('preventionStrategies', language)}
            </h3>
            <div className="space-y-3">
              {preventions.map((prevention, index) => (
                <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h4 className="font-medium text-green-900 mb-2">{prevention.title}</h4>
                  <p className="text-sm text-gray-700 mb-3">{prevention.description}</p>
                  <div className="text-xs text-gray-600 space-y-1">
                    <p><strong>{getTranslation('benefits', language)}:</strong> {prevention.expected_benefits}</p>
                    <p><strong>{getTranslation('difficulty', language)}:</strong>
                      <span className={`ml-1 px-2 py-1 rounded ${
                        prevention.difficulty_level === 'easy' ? 'bg-green-100 text-green-800' :
                        prevention.difficulty_level === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {prevention.difficulty_level}
                      </span>
                    </p>
                  </div>
                  {prevention.implementation_steps && prevention.implementation_steps.length > 0 && (
                    <div className="mt-3">
                      <p className="text-xs font-medium text-gray-700 mb-1">{getTranslation('steps', language)}:</p>
                      <ol className="text-xs text-gray-600 list-decimal list-inside space-y-1">
                        {prevention.implementation_steps.map((step, stepIndex) => (
                          <li key={stepIndex}>{step}</li>
                        ))}
                      </ol>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* References Section */}
        {(treatments.length > 0 || preventions.length > 0) && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <span className="mr-2">📚</span>
              {getTranslation('referencesSources', language) || 'References & Sources'}
            </h3>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-3">{getTranslation('officialAgriculturalReferences', language) || 'Official Agricultural References'}</h4>
              <div className="space-y-3">
                <div className="bg-white rounded-lg p-3 border border-blue-100">
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
                        <span className="text-orange-600 font-bold text-sm">T</span>
                      </div>
                    </div>
                    <div className="flex-1">
                      <h5 className="font-medium text-gray-900">Tamil Nadu Agricultural University (TNAU)</h5>
                      <p className="text-sm text-gray-600 mb-2">Official source for crop protection and disease management</p>
                      <a
                        href="https://agritech.tnau.ac.in/crop_protection/crop_prot_crop%20diseases_cereals_rice_main.html"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 font-medium"
                      >
                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                        Visit TNAU Crop Protection
                      </a>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg p-3 border border-blue-100">
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                        <span className="text-green-600 font-bold text-sm">I</span>
                      </div>
                    </div>
                    <div className="flex-1">
                      <h5 className="font-medium text-gray-900">ICAR Guidelines</h5>
                      <p className="text-sm text-gray-600 mb-2">Indian Council of Agricultural Research recommendations</p>
                      <a
                        href="https://icar.org.in/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 font-medium"
                      >
                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                        Visit ICAR Website
                      </a>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg p-3 border border-blue-100">
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                        <span className="text-purple-600 font-bold text-sm">W</span>
                      </div>
                    </div>
                    <div className="flex-1">
                      <h5 className="font-medium text-gray-900">WHO Guidelines</h5>
                      <p className="text-sm text-gray-600 mb-2">World Health Organization pesticide safety guidelines</p>
                      <a
                        href="https://www.who.int/health-topics/pesticides"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 font-medium"
                      >
                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                        WHO Pesticide Guidelines
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <svg className="w-5 h-5 text-yellow-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h5 className="text-sm font-medium text-yellow-800">{getTranslation('importantNotice', language) || 'Important Notice'}</h5>
                    <p className="text-sm text-yellow-700 mt-1">
                      Always consult local agricultural extension services before applying any treatments.
                      Product availability and regulations may vary by region.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}
      </div>

    </div>
  );
};

export default CropPredictor;