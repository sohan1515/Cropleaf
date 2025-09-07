import { getTranslation } from '../translations';
import RiceDiseasesInfo from './RiceDiseasesInfo';

const TNAUModal = ({ isOpen, onClose, language = 'en' }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-6xl h-[90vh] flex flex-col">
        {/* Modal Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Plant Diseases Information</h2>
            <p className="text-sm text-gray-600 mt-1">Comprehensive guide to major plant diseases and their management</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Modal Content */}
        <div className="flex-1 overflow-y-auto">
          <RiceDiseasesInfo />
        </div>

        {/* Modal Footer */}
        <div className="border-t border-gray-200 p-6 flex justify-between items-center">
          <div className="text-sm text-gray-600">
            Comprehensive rice diseases information and management guide
          </div>
          <button
            onClick={onClose}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 font-medium"
          >
            {getTranslation('close', language)}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TNAUModal;