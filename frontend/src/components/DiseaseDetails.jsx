import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { getTranslation } from '../translations';

const DiseaseDetails = ({ language }) => {
  const { diseaseName } = useParams();
  const navigate = useNavigate();
  const [diseaseData, setDiseaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchDiseaseDetails();
  }, [diseaseName]);

  const fetchDiseaseDetails = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/api/disease/${diseaseName}/`);
      setDiseaseData(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching disease details:', err);
      setError(getTranslation('failedToLoadDisease', language));
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-100 to-blue-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center space-x-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
            <span className="text-lg text-gray-700">{getTranslation('loading', language)}</span>
          </div>
        </div>
      </div>
    );
  }

  if (error || !diseaseData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-100 to-blue-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
          <div className="text-center">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">
              {getTranslation('error', language)}
            </h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition duration-200"
            >
              {getTranslation('backToHome', language)}
            </button>
          </div>
        </div>
      </div>
    );
  }

  const { disease, treatments, preventions } = diseaseData;

  const tabs = [
    { id: 'overview', label: getTranslation('overview', language), icon: '📋' },
    { id: 'symptoms', label: getTranslation('symptoms', language), icon: '🔍' },
    { id: 'causes', label: getTranslation('causes', language), icon: '🦠' },
    { id: 'management', label: getTranslation('management', language), icon: '🛠️' },
    { id: 'treatments', label: getTranslation('treatments', language), icon: '💊' },
    { id: 'prevention', label: getTranslation('prevention', language), icon: '🛡️' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-100 to-blue-100">
      {/* Header */}
      <div className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/')}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition duration-200"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>{getTranslation('back', language)}</span>
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{disease.name}</h1>
                {disease.scientific_name && (
                  <p className="text-lg text-gray-600 italic">{disease.scientific_name}</p>
                )}
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                disease.prevention_priority === 'high' ? 'bg-red-100 text-red-800' :
                disease.prevention_priority === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {disease.prevention_priority} {getTranslation('priority', language)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4">
          <nav className="flex space-x-8 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-8">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">{getTranslation('overview', language)}</h2>
                  <p className="text-gray-700 leading-relaxed">{disease.description}</p>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">{getTranslation('affectedCrops', language)}</h3>
                    <div className="flex flex-wrap gap-2">
                      {disease.affected_crops.map((crop, index) => (
                        <span key={index} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                          {crop}
                        </span>
                      ))}
                    </div>
                  </div>

                  {disease.economic_impact && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">{getTranslation('economicImpact', language)}</h3>
                      <p className="text-gray-700">{disease.economic_impact}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'symptoms' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{getTranslation('symptoms', language)}</h2>

                <div className="grid md:grid-cols-3 gap-4 mb-6">
                  {Object.entries(disease.severity_levels).map(([level, description]) => (
                    <div key={level} className={`p-4 rounded-lg border-2 ${
                      level === 'mild' ? 'border-green-200 bg-green-50' :
                      level === 'moderate' ? 'border-yellow-200 bg-yellow-50' :
                      'border-red-200 bg-red-50'
                    }`}>
                      <h3 className={`font-semibold capitalize ${
                        level === 'mild' ? 'text-green-800' :
                        level === 'moderate' ? 'text-yellow-800' :
                        'text-red-800'
                      }`}>
                        {level} {getTranslation('severity', language)}
                      </h3>
                      <p className="text-sm mt-1">{description}</p>
                    </div>
                  ))}
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">{getTranslation('symptomList', language)}</h3>
                  <ul className="grid md:grid-cols-2 gap-2">
                    {disease.symptoms.map((symptom, index) => (
                      <li key={index} className="flex items-center space-x-2">
                        <span className="text-red-500">•</span>
                        <span className="text-gray-700">{symptom}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {activeTab === 'causes' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{getTranslation('causes', language)}</h2>

                <div className="grid md:grid-cols-2 gap-6">
                  {disease.causal_agent && (
                    <div className="bg-blue-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold text-blue-900 mb-2">{getTranslation('causalAgent', language)}</h3>
                      <p className="text-blue-800">{disease.causal_agent}</p>
                    </div>
                  )}

                  {disease.host_range && (
                    <div className="bg-purple-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold text-purple-900 mb-2">{getTranslation('hostRange', language)}</h3>
                      <p className="text-purple-800">{disease.host_range}</p>
                    </div>
                  )}

                  {disease.environmental_conditions && (
                    <div className="bg-green-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold text-green-900 mb-2">{getTranslation('environmentalConditions', language)}</h3>
                      <p className="text-green-800">{disease.environmental_conditions}</p>
                    </div>
                  )}

                  {disease.disease_cycle && (
                    <div className="bg-orange-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold text-orange-900 mb-2">{getTranslation('diseaseCycle', language)}</h3>
                      <p className="text-orange-800">{disease.disease_cycle}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'management' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{getTranslation('management', language)}</h2>

                <div className="grid md:grid-cols-1 gap-6">
                  {disease.cultural_control && (
                    <div className="bg-green-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold text-green-900 mb-3 flex items-center">
                        <span className="mr-2">🌱</span>
                        {getTranslation('culturalControl', language)}
                      </h3>
                      <p className="text-green-800">{disease.cultural_control}</p>
                    </div>
                  )}

                  {disease.chemical_control && (
                    <div className="bg-blue-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold text-blue-900 mb-3 flex items-center">
                        <span className="mr-2">🧪</span>
                        {getTranslation('chemicalControl', language)}
                      </h3>
                      <p className="text-blue-800">{disease.chemical_control}</p>
                    </div>
                  )}

                  {disease.biological_control && (
                    <div className="bg-purple-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold text-purple-900 mb-3 flex items-center">
                        <span className="mr-2">🦠</span>
                        {getTranslation('biologicalControl', language)}
                      </h3>
                      <p className="text-purple-800">{disease.biological_control}</p>
                    </div>
                  )}

                  {disease.integrated_management && (
                    <div className="bg-indigo-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold text-indigo-900 mb-3 flex items-center">
                        <span className="mr-2">🎯</span>
                        {getTranslation('integratedManagement', language)}
                      </h3>
                      <p className="text-indigo-800">{disease.integrated_management}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'treatments' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{getTranslation('treatments', language)}</h2>

                {treatments.length === 0 ? (
                  <p className="text-gray-600">{getTranslation('noTreatments', language)}</p>
                ) : (
                  <div className="space-y-4">
                    {treatments.map((treatment) => (
                      <div key={treatment.id} className="border border-gray-200 rounded-lg p-6">
                        <div className="flex justify-between items-start mb-4">
                          <div>
                            <h3 className="text-lg font-semibold text-gray-900">{treatment.name}</h3>
                            <span className={`inline-block mt-2 px-3 py-1 text-sm rounded-full ${
                              treatment.treatment_type === 'chemical' ? 'bg-red-100 text-red-800' :
                              treatment.treatment_type === 'organic' ? 'bg-green-100 text-green-800' :
                              treatment.treatment_type === 'biological' ? 'bg-purple-100 text-purple-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {treatment.treatment_type}
                            </span>
                          </div>
                          <div className="flex items-center">
                            <span className="text-sm text-gray-600 mr-2">{getTranslation('effectiveness', language)}:</span>
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

                        <p className="text-gray-700 mb-4">{treatment.description}</p>

                        <div className="grid md:grid-cols-2 gap-4 text-sm">
                          <div>
                            <strong className="text-gray-900">{getTranslation('application', language)}:</strong>
                            <p className="text-gray-700 mt-1">{treatment.application_method}</p>
                          </div>
                          {treatment.cost_estimate && (
                            <div>
                              <strong className="text-gray-900">{getTranslation('cost', language)}:</strong>
                              <p className="text-gray-700 mt-1">${treatment.cost_estimate}</p>
                            </div>
                          )}
                        </div>

                        {treatment.safety_precautions && (
                          <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
                            <strong className="text-yellow-800">{getTranslation('safety', language)}:</strong>
                            <p className="text-yellow-700 mt-1">{treatment.safety_precautions}</p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'prevention' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{getTranslation('prevention', language)}</h2>

                {preventions.length === 0 ? (
                  <p className="text-gray-600">{getTranslation('noPrevention', language)}</p>
                ) : (
                  <div className="space-y-4">
                    {preventions.map((prevention) => (
                      <div key={prevention.id} className="border border-gray-200 rounded-lg p-6">
                        <div className="flex justify-between items-start mb-4">
                          <h3 className="text-lg font-semibold text-gray-900">{prevention.title}</h3>
                          <div className="flex items-center space-x-2">
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              prevention.difficulty_level === 'easy' ? 'bg-green-100 text-green-800' :
                              prevention.difficulty_level === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {prevention.difficulty_level}
                            </span>
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              prevention.cost_impact === 'low' ? 'bg-green-100 text-green-800' :
                              prevention.cost_impact === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {prevention.cost_impact}
                            </span>
                          </div>
                        </div>

                        <p className="text-gray-700 mb-4">{prevention.description}</p>

                        <div className="mb-4">
                          <strong className="text-gray-900">{getTranslation('benefits', language)}:</strong>
                          <p className="text-gray-700 mt-1">{prevention.expected_benefits}</p>
                        </div>

                        {prevention.implementation_steps && prevention.implementation_steps.length > 0 && (
                          <div>
                            <strong className="text-gray-900">{getTranslation('steps', language)}:</strong>
                            <ol className="mt-2 space-y-1">
                              {prevention.implementation_steps.map((step, index) => (
                                <li key={index} className="flex items-start space-x-2">
                                  <span className="text-blue-600 font-medium">{index + 1}.</span>
                                  <span className="text-gray-700">{step}</span>
                                </li>
                              ))}
                            </ol>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DiseaseDetails;