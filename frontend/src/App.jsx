import { useState, useEffect } from 'react';
import CropPredictor from './components/CropPredictor'
import LanguageSelector from './components/LanguageSelector'
import RiceDiseasesInfo from './components/RiceDiseasesInfo'
import Dashboard from './components/Dashboard'
import UserAuth from './components/UserAuth'
import Marketplace from './components/Marketplace'
import NotificationsPanel from './components/NotificationsPanel'
import { getTranslation } from './translations'

function App() {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeView, setActiveView] = useState('predictor');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [notificationsOpen, setNotificationsOpen] = useState(false);

  useEffect(() => {
    // Load saved language preference
    const savedLanguage = localStorage.getItem('selectedLanguage');
    if (savedLanguage) {
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  const handleLanguageChange = (newLanguage) => {
    setCurrentLanguage(newLanguage);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-100 to-blue-100">
      {/* Main Sidebar */}
      <div className={`fixed left-0 top-0 h-screen bg-gradient-to-b from-green-600 to-blue-600 text-white shadow-xl z-50 transition-all duration-300 ease-in-out overflow-hidden ${
        sidebarCollapsed ? 'w-16' : 'w-80'
      }`}>
        <div className="p-4 h-full flex flex-col">
          {/* Header with Toggle */}
          <div className="flex items-center justify-between mb-6">
            {!sidebarCollapsed && (
              <h2 className="text-xl font-bold">🌾 CropLeaf</h2>
            )}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="p-2 rounded-lg hover:bg-white/20 transition-colors duration-200"
            >
              {sidebarCollapsed ? '→' : '←'}
            </button>
          </div>

          {!sidebarCollapsed && (
            <div className="opacity-100 transition-opacity duration-300 flex-1 overflow-y-auto">
              {/* Language Selector */}
              <div className="mb-6">
                <h3 className="text-sm font-semibold mb-3 flex items-center">
                  <span className="mr-2">🌍</span>
                  {getTranslation('language', currentLanguage)}
                </h3>
                <LanguageSelector onLanguageChange={handleLanguageChange} />
              </div>

              {/* Navigation */}
              <div className="mb-6">
                <h3 className="text-sm font-semibold mb-3 flex items-center">
                  <span className="mr-2">🧭</span>
                  {getTranslation('navigation', currentLanguage)}
                </h3>
                <div className="space-y-2">
                  <button
                    onClick={() => {
                      setActiveView('predictor');
                      setSidebarCollapsed(true);
                    }}
                    className={`w-full text-left p-4 rounded-lg transition-all duration-200 ${
                      activeView === 'predictor'
                        ? 'bg-white text-green-600 shadow-md'
                        : 'bg-white/10 hover:bg-white/20'
                    }`}
                  >
                    <div className="flex items-center mb-2">
                      <span className="mr-3 text-xl">🔬</span>
                      <div>
                        <div className="font-medium">{getTranslation('diseasePredictor', currentLanguage)}</div>
                        <div className="text-xs opacity-75">{getTranslation('uploadAnalyzeImages', currentLanguage)}</div>
                      </div>
                    </div>
                    <p className="text-xs opacity-80 mt-2">
                      {getTranslation('aiPoweredAnalysis', currentLanguage)}
                    </p>
                  </button>

                  <button
                    onClick={() => {
                      setActiveView('dashboard');
                      setSidebarCollapsed(true);
                    }}
                    className={`w-full text-left p-4 rounded-lg transition-all duration-200 ${
                      activeView === 'dashboard'
                        ? 'bg-white text-green-600 shadow-md'
                        : 'bg-white/10 hover:bg-white/20'
                    }`}
                  >
                    <div className="flex items-center mb-2">
                      <span className="mr-3 text-xl">📊</span>
                      <div>
                        <div className="font-medium">{getTranslation('dashboard', currentLanguage)}</div>
                        <div className="text-xs opacity-75">Analytics & insights</div>
                      </div>
                    </div>
                    <p className="text-xs opacity-80 mt-2">
                      {getTranslation('comprehensiveAnalytics', currentLanguage)}
                    </p>
                  </button>

                  <button
                    onClick={() => {
                      setActiveView('diseases');
                      setSidebarCollapsed(true);
                    }}
                    className={`w-full text-left p-4 rounded-lg transition-all duration-200 ${
                      activeView === 'diseases'
                        ? 'bg-white text-green-600 shadow-md'
                        : 'bg-white/10 hover:bg-white/20'
                    }`}
                  >
                    <div className="flex items-center mb-2">
                      <span className="mr-3 text-xl">📚</span>
                      <div>
                        <div className="font-medium">{getTranslation('plantDiseasesInfo', currentLanguage)}</div>
                        <div className="text-xs opacity-75">{getTranslation('comprehensiveDiseaseDatabase', currentLanguage)}</div>
                      </div>
                    </div>
                    <p className="text-xs opacity-80 mt-2">
                      {getTranslation('exploreDiseaseInfo', currentLanguage)}
                    </p>
                  </button>

                  <button
                    onClick={() => {
                      setActiveView('marketplace');
                      setSidebarCollapsed(true);
                    }}
                    className={`w-full text-left p-4 rounded-lg transition-all duration-200 ${
                      activeView === 'marketplace'
                        ? 'bg-white text-green-600 shadow-md'
                        : 'bg-white/10 hover:bg-white/20'
                    }`}
                  >
                    <div className="flex items-center mb-2">
                      <span className="mr-3 text-xl">🛒</span>
                      <div>
                        <div className="font-medium">{getTranslation('marketplace', currentLanguage)}</div>
                        <div className="text-xs opacity-75">Buy & sell agricultural products</div>
                      </div>
                    </div>
                    <p className="text-xs opacity-80 mt-2">
                      {getTranslation('connectSellersBuyers', currentLanguage)}
                    </p>
                  </button>

                  <button
                    onClick={() => {
                      setActiveView('auth');
                      setSidebarCollapsed(true);
                    }}
                    className={`w-full text-left p-4 rounded-lg transition-all duration-200 ${
                      activeView === 'auth'
                        ? 'bg-white text-green-600 shadow-md'
                        : 'bg-white/10 hover:bg-white/20'
                    }`}
                  >
                    <div className="flex items-center mb-2">
                      <span className="mr-3 text-xl">👤</span>
                      <div>
                        <div className="font-medium">{getTranslation('account', currentLanguage)}</div>
                        <div className="text-xs opacity-75">{isLoggedIn ? `Welcome, ${user?.username || 'User'}` : getTranslation('signInAccessFeatures', currentLanguage)}</div>
                      </div>
                    </div>
                    <p className="text-xs opacity-80 mt-2">
                      {isLoggedIn ? getTranslation('viewProfileHistory', currentLanguage) : getTranslation('createPersonalizedExperience', currentLanguage)}
                    </p>
                  </button>
                </div>
              </div>

              {/* Quick Stats */}
              <div className="mb-6">
                <h3 className="text-sm font-semibold mb-3 flex items-center">
                  <span className="mr-2">📊</span>
                  {getTranslation('statistics', currentLanguage)}
                </h3>
                <div className="bg-white/10 rounded-lg p-4 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">{getTranslation('totalCrops', currentLanguage)}</span>
                    <span className="font-bold text-yellow-300">8</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">{getTranslation('totalDiseases', currentLanguage)}</span>
                    <span className="font-bold text-yellow-300">9</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">{getTranslation('languages', currentLanguage)}</span>
                    <span className="font-bold text-yellow-300">50+</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">{getTranslation('aiAccuracy', currentLanguage)}</span>
                    <span className="font-bold text-green-300">95%</span>
                  </div>
                </div>
              </div>

              {/* Features */}
              <div className="mb-6">
                <h3 className="text-sm font-semibold mb-3 flex items-center">
                  <span className="mr-2">✨</span>
                  {getTranslation('features', currentLanguage)}
                </h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center">
                    <span className="mr-2">🖼️</span>
                    <span>{getTranslation('imageAnalysis', currentLanguage)}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="mr-2">🌐</span>
                    <span>{getTranslation('multiLanguage', currentLanguage)}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="mr-2">📱</span>
                    <span>{getTranslation('mobileFriendly', currentLanguage)}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="mr-2">🔬</span>
                    <span>{getTranslation('researchBased', currentLanguage)}</span>
                  </div>
                </div>
              </div>

              {/* Footer */}
              <div className="mt-auto pt-6 border-t border-white/20">
                <div className="text-xs text-white/70 text-center">
                  <p>🌱 Empowering Farmers Worldwide</p>
                  <p className="mt-1">Version 2.0</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className={`transition-all duration-300 ease-in-out min-h-screen overflow-y-auto ${
        sidebarCollapsed ? 'ml-16' : 'ml-80'
      }`}>
        <div className="min-h-screen p-4 py-8">
          <div className="w-full max-w-6xl mx-auto">
            {/* Content Header */}
            <header className="text-center mb-8 relative">
              <div className="absolute top-0 right-0">
                <button
                  onClick={() => setNotificationsOpen(true)}
                  className="p-2 bg-white rounded-full shadow-md hover:shadow-lg transition-shadow"
                  title={getTranslation('notifications', currentLanguage) || 'Notifications'}
                >
                  <span className="text-xl">🔔</span>
                </button>
              </div>
              <h1 className="text-4xl font-bold text-gray-800 mb-2">
                {activeView === 'predictor'
                  ? getTranslation('title', currentLanguage)
                  : activeView === 'dashboard'
                  ? getTranslation('agriculturalDashboard', currentLanguage)
                  : activeView === 'marketplace'
                  ? getTranslation('marketplace', currentLanguage)
                  : getTranslation('plantDiseasesInfo', currentLanguage)
                }
              </h1>
              <p className="text-lg text-gray-600">
                {activeView === 'predictor'
                  ? getTranslation('subtitle', currentLanguage)
                  : activeView === 'dashboard'
                  ? getTranslation('comprehensiveAnalytics', currentLanguage)
                  : activeView === 'marketplace'
                  ? getTranslation('connectSellersBuyers', currentLanguage)
                  : getTranslation('comprehensiveGuide', currentLanguage)
                }
              </p>
            </header>

            {/* Content Area */}
            <div className="mb-8">
              {activeView === 'predictor' ? (
                <CropPredictor language={currentLanguage} />
              ) : activeView === 'dashboard' ? (
                <Dashboard language={currentLanguage} />
              ) : activeView === 'marketplace' ? (
                <Marketplace language={currentLanguage} />
              ) : activeView === 'auth' ? (
                <UserAuth
                  language={currentLanguage}
                  onAuthSuccess={(data) => {
                    setIsLoggedIn(true);
                    setUser(data.user);
                    setActiveView('predictor');
                  }}
                />
              ) : (
                <RiceDiseasesInfo language={currentLanguage} />
              )}
            </div>

            {/* Footer */}
            <footer className="text-center mt-8 text-gray-500">
              <p>{getTranslation('poweredBy', currentLanguage)}</p>
            </footer>
          </div>
        </div>
      </div>

      {/* Notifications Panel */}
      <NotificationsPanel
        language={currentLanguage}
        isOpen={notificationsOpen}
        onClose={() => setNotificationsOpen(false)}
      />
    </div>
  )
}

export default App
