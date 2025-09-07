import { useState, useEffect } from 'react';
import { getTranslation } from '../translations';

const LanguageSelector = ({ onLanguageChange }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [isOpen, setIsOpen] = useState(false);

  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'mr', name: 'मराठी', flag: '🇮🇳' },
    { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
    { code: 'gu', name: 'ગુજરાતી', flag: '🇮🇳' },
    { code: 'pa', name: 'ਪੰਜਾਬੀ', flag: '🇮🇳' },
    { code: 'es', name: 'Español', flag: '🇪🇸' }
  ];

  const changeLanguage = (langCode) => {
    console.log('Changing language to:', langCode);
    setCurrentLanguage(langCode);
    setIsOpen(false);

    // Store language preference in localStorage
    localStorage.setItem('selectedLanguage', langCode);

    // Notify parent component
    if (onLanguageChange) {
      onLanguageChange(langCode);
    }

    // Show success message
    const successMessage = document.createElement('div');
    successMessage.textContent = getTranslation('successMessage', langCode);
    successMessage.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #10b981; color: white; padding: 10px 20px; border-radius: 5px; z-index: 10000; font-size: 14px;';
    document.body.appendChild(successMessage);
    setTimeout(() => document.body.removeChild(successMessage), 2000);
  };

  const resetToEnglish = () => {
    changeLanguage('en');
    if (onLanguageChange) {
      onLanguageChange('en');
    }
  };

  useEffect(() => {
    // Load saved language preference
    const savedLanguage = localStorage.getItem('selectedLanguage');
    if (savedLanguage && languages.some(lang => lang.code === savedLanguage)) {
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  const currentLang = languages.find(lang => lang.code === currentLanguage) || languages[0];

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 bg-white/20 backdrop-blur-sm border border-white/30 rounded-lg px-3 py-2 hover:bg-white/30 transition duration-200 w-full text-left"
        title="Click to change language"
      >
        <span className="text-lg">{currentLang.flag}</span>
        <span className="text-sm font-medium text-white flex-1">{currentLang.name}</span>
        <svg
          className={`w-4 h-4 transition-transform duration-200 text-white ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-full mt-2 w-full bg-white/95 backdrop-blur-sm border border-white/30 rounded-lg shadow-lg z-50">
          {languages.map((language) => (
            <button
              key={language.code}
              onClick={() => changeLanguage(language.code)}
              className={`w-full flex items-center space-x-3 px-4 py-3 text-left hover:bg-white/80 transition duration-150 ${
                currentLanguage === language.code ? 'bg-green-100 text-green-700' : 'text-gray-800'
              }`}
            >
              <span className="text-lg">{language.flag}</span>
              <span className="text-sm font-medium">{language.name}</span>
              {currentLanguage === language.code && (
                <svg className="w-4 h-4 ml-auto text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          ))}

          <div className="border-t border-gray-300 my-1"></div>

          <button
            onClick={resetToEnglish}
            className="w-full flex items-center space-x-3 px-4 py-3 text-left hover:bg-white/80 transition duration-150 text-gray-800"
          >
            <span className="text-lg">🔄</span>
            <span className="text-sm font-medium">Reset to English</span>
          </button>
        </div>
      )}

      {/* Click outside to close */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsOpen(false)}
        ></div>
      )}
    </div>
  );
};

export default LanguageSelector;