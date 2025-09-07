import { useState, useEffect } from 'react';
import { getTranslation } from '../translations';
import { Wrapper, Status } from '@googlemaps/react-wrapper';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Haversine formula for distance calculation
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Radius of the Earth in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a =
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  const distance = R * c; // Distance in kilometers
  return distance * 1000; // Convert to meters
};

const Marketplace = ({ language = 'en' }) => {
  const [products, setProducts] = useState([]);
  const [mandis, setMandis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [sortBy, setSortBy] = useState('newest');
  const [showMap, setShowMap] = useState(false);
  const [userLocation, setUserLocation] = useState(null);
  const [selectedMandi, setSelectedMandi] = useState(null);
  const [showMandiModal, setShowMandiModal] = useState(false);
  const [locationLoading, setLocationLoading] = useState(false);
  const [locationError, setLocationError] = useState(null);

  useEffect(() => {
    fetchProducts();
    fetchMandis();
    getUserLocation();
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [searchQuery, selectedCategory, sortBy]);

  const fetchProducts = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/marketplace/products/?search=${searchQuery}&type=${selectedCategory}&sort=${sortBy}`, {
        credentials: 'include'
      });
      const data = await response.json();
      setProducts(data.products || []);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const fetchMandis = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/marketplace/mandis/', {
        credentials: 'include'
      });
      const data = await response.json();
      setMandis(data.mandis || []);
    } catch (error) {
      console.error('Error fetching mandis:', error);
    } finally {
      setLoading(false);
    }
  };

  const getUserLocation = () => {
    if (!navigator.geolocation) {
      console.warn('Geolocation is not supported by this browser');
      setLocationError('Geolocation is not supported by this browser');
      return;
    }

    setLocationLoading(true);
    setLocationError(null);
    console.log('Requesting location permission...');

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const location = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        console.log('Location obtained:', location);
        setUserLocation(location);
        setLocationLoading(false);
        setLocationError(null);
      },
      (error) => {
        console.error('Geolocation error:', error);
        setLocationLoading(false);

        let errorMessage = 'Unable to get your location';

        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location access denied. Please enable location permissions in your browser settings and try again.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information is unavailable. Please check your GPS settings and try again.';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timed out. Please try again.';
            break;
          default:
            errorMessage = 'An unknown error occurred while retrieving location.';
            break;
        }

        setLocationError(errorMessage);
        alert(errorMessage);
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 300000 // 5 minutes
      }
    );
  };

  const handleProductInquiry = async () => {
    // This would require user authentication
    alert('Please log in to send inquiries to sellers');
  };

  const handleViewLocation = (mandi) => {
    setSelectedMandi(mandi);
    setShowMandiModal(true);
  };

  const openInGoogleMaps = (mandi) => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${mandi.latitude},${mandi.longitude}`;
    window.open(url, '_blank');
  };

  const categories = [
    { value: '', label: getTranslation('allCategories', language) },
    { value: 'crop', label: 'Crops' },
    { value: 'seed', label: 'Seeds' },
    { value: 'fertilizer', label: 'Fertilizer' },
    { value: 'equipment', label: 'Equipment' }
  ];

  const sortOptions = [
    { value: 'newest', label: getTranslation('newestFirst', language) },
    { value: 'price_low', label: getTranslation('priceLowToHigh', language) },
    { value: 'price_high', label: 'Price: High to Low' }
  ];

  const getQualityBadgeColor = (grade) => {
    switch (grade) {
      case 'a': return 'bg-green-100 text-green-800';
      case 'b': return 'bg-yellow-100 text-yellow-800';
      case 'c': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderMap = (status) => {
    if (status === Status.LOADING) return <div>Loading map...</div>;
    if (status === Status.FAILURE) return <div>Error loading map</div>;
    return null;
  };

  // Check if we have a valid Google Maps API key
  const hasApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY &&
                   import.meta.env.VITE_GOOGLE_MAPS_API_KEY !== "YOUR_REAL_API_KEY_HERE" &&
                   import.meta.env.VITE_GOOGLE_MAPS_API_KEY !== "DEMO_KEY";

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6 min-h-full">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{getTranslation('marketplace', language)}</h1>
        <p className="text-gray-600">
          {getTranslation('connectSellersBuyers', language)}
        </p>
      </div>

      {/* Controls */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex flex-col lg:flex-row gap-4 mb-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder={getTranslation('searchProducts', language)}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            {categories.map(cat => (
              <option key={cat.value} value={cat.value}>{cat.label}</option>
            ))}
          </select>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            {sortOptions.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <button
            onClick={() => setShowMap(!showMap)}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-200"
          >
            🗺️ {showMap ? 'Hide Map' : 'Show Map'}
          </button>
        </div>

        {/* Quality Assurance Banner */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-green-800">AI-Powered Quality Verification</h4>
              <p className="text-sm text-green-700 mt-1">
                All products listed here have been verified using our AI disease detection system to ensure quality and health.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Map Section */}
      {showMap && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Nearest Mandi Locations</h3>
          <div className="h-96">
            {hasApiKey ? (
              <Wrapper
                apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}
                render={renderMap}
              >
                <MapComponent mandis={mandis} userLocation={userLocation} />
              </Wrapper>
            ) : (
              <OpenStreetMapComponent mandis={mandis} userLocation={userLocation} />
            )}
            {/* Location Status and Controls */}
            <div className="mt-4 space-y-3">
              {/* Map Status */}
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h4 className="text-sm font-medium text-green-800">
                      🗺️ {hasApiKey ? 'Google Maps Active' : 'OpenStreetMap Active (Free)'}
                    </h4>
                    <p className="text-sm text-green-700 mt-1">
                      {hasApiKey
                        ? 'Using Google Maps for enhanced navigation features.'
                        : 'Using free OpenStreetMap for interactive navigation. No API key required!'
                      }
                    </p>
                  </div>
                </div>
              </div>

              {/* Location Status */}
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      {locationLoading ? (
                        <svg className="w-5 h-5 text-blue-600 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                      ) : userLocation ? (
                        <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                      ) : (
                        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      )}
                    </div>
                    <div className="ml-3">
                      <h4 className="text-sm font-medium text-blue-800">
                        📍 Your Location
                      </h4>
                      <p className="text-sm text-blue-700 mt-1">
                        {locationLoading
                          ? 'Getting your location...'
                          : userLocation
                            ? `Location detected: ${userLocation.lat.toFixed(4)}, ${userLocation.lng.toFixed(4)}`
                            : locationError || 'Click "Find My Location" to enable distance-based numbering'
                        }
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={getUserLocation}
                    disabled={locationLoading}
                    className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed transition-colors"
                  >
                    {locationLoading ? '🔄 Getting...' : userLocation ? '🔄 Refresh' : '📍 Find Me'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Products Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <div key={product.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition duration-200">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">{product.title}</h3>
                  <p className="text-2xl font-bold text-green-600">₹{product.price_per_unit}/{product.unit}</p>
                  <p className="text-sm text-gray-600">Total: ₹{product.total_price?.toLocaleString()}</p>
                </div>
                <div className="flex flex-col items-end space-y-2">
                  <span className={`inline-block px-3 py-1 text-xs font-semibold rounded-full ${getQualityBadgeColor(product.quality_grade)}`}>
                    Grade {product.quality_grade.toUpperCase()}
                  </span>
                  {product.ai_verified && (
                    <span className="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                      AI Verified
                    </span>
                  )}
                </div>
              </div>

              <div className="space-y-2 mb-4">
                <div className="flex items-center text-sm text-gray-600">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  {product.seller.first_name} {product.seller.last_name}
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {product.location}
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                  {product.quantity} {product.unit} available
                </div>
                {product.nearest_mandi && (
                  <div className="flex items-center text-sm text-gray-600">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    Nearest: {product.nearest_mandi.name}
                  </div>
                )}
              </div>

              <div className="flex space-x-2">
                <button
                  onClick={() => handleProductInquiry(product.id)}
                  className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition duration-200"
                >
                  Contact Seller
                </button>
                <button
                  onClick={() => handleViewLocation(product.nearest_mandi)}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition duration-200"
                >
                  📍 View Location
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Marketplace Stats */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Marketplace Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{products.length}</div>
            <div className="text-sm text-gray-600">Active Products</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{mandis.length}</div>
            <div className="text-sm text-gray-600">Mandi Locations</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">
              {products.filter(p => p.ai_verified).length}
            </div>
            <div className="text-sm text-gray-600">AI Verified</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {new Set(products.map(p => p.seller.id)).size}
            </div>
            <div className="text-sm text-gray-600">Active Sellers</div>
          </div>
        </div>
      </div>

      {/* Mandi Details Modal */}
      {showMandiModal && selectedMandi && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{selectedMandi.name}</h2>
                  <p className="text-gray-600">{selectedMandi.district}, {selectedMandi.state}</p>
                </div>
                <button
                  onClick={() => setShowMandiModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Mandi Details */}
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">📍 Location Details</h3>
                    <p className="text-gray-600">{selectedMandi.address || 'Address not available'}</p>
                    <p className="text-sm text-gray-500 mt-2">
                      Coordinates: {selectedMandi.latitude || 'N/A'}, {selectedMandi.longitude || 'N/A'}
                    </p>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">📞 Contact Information</h3>
                    <p className="text-gray-600">Phone: {selectedMandi.contact_number || 'Not available'}</p>
                    <p className="text-gray-600">Hours: {selectedMandi.operating_hours || 'Not specified'}</p>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">🏢 Facilities</h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedMandi.facilities && selectedMandi.facilities.length > 0 ? (
                        selectedMandi.facilities.map((facility, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                          >
                            {facility}
                          </span>
                        ))
                      ) : (
                        <span className="text-gray-500 text-sm">No facilities information available</span>
                      )}
                    </div>
                  </div>

                  <div className="flex space-x-3">
                    <button
                      onClick={() => openInGoogleMaps(selectedMandi)}
                      className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition duration-200 flex items-center justify-center"
                    >
                      🗺️ Get Directions
                    </button>
                    <button
                      onClick={() => window.open(`tel:${selectedMandi.contact_number}`, '_self')}
                      className="flex-1 bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 transition duration-200 flex items-center justify-center"
                    >
                      📞 Call Now
                    </button>
                  </div>
                </div>

                {/* Google Maps */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">🗺️ Location Map</h3>
                  <div className="h-96 bg-gray-100 rounded-lg">
                    <Wrapper
                      apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "DEMO_KEY"}
                      render={renderMap}
                    >
                      <MandiDetailMap mandi={selectedMandi} userLocation={userLocation} />
                    </Wrapper>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Map Component with user location centric view
const MapComponent = ({ mandis, userLocation }) => {
  const hasApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY && import.meta.env.VITE_GOOGLE_MAPS_API_KEY !== "DEMO_KEY";

  useEffect(() => {
    // Initialize Google Map only if API key is available
    if (hasApiKey && window.google && mandis.length > 0) {
      // Calculate bounds to include all mandis and user location
      const bounds = new window.google.maps.LatLngBounds();

      // Add user location to bounds if available
      if (userLocation) {
        bounds.extend(new window.google.maps.LatLng(userLocation.lat, userLocation.lng));
      }

      // Add all mandi locations to bounds
      mandis.forEach(mandi => {
        bounds.extend(new window.google.maps.LatLng(
          parseFloat(mandi.latitude),
          parseFloat(mandi.longitude)
        ));
      });

      const map = new window.google.maps.Map(document.getElementById('marketplace-map'), {
        center: userLocation || bounds.getCenter(), // Center on user location or bounds center
        zoom: userLocation ? 10 : 5, // Closer zoom if user location available
      });

      // Fit map to show all markers
      if (mandis.length > 1 || userLocation) {
        map.fitBounds(bounds);
      }

      // Add user location marker if available
      if (userLocation) {
        const userMarker = new window.google.maps.Marker({
          position: userLocation,
          map: map,
          title: 'Your Location',
          icon: {
            url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" fill="#3B82F6" stroke="white" stroke-width="3"/>
                <circle cx="12" cy="12" r="4" fill="white"/>
                <circle cx="12" cy="8" r="2" fill="#3B82F6"/>
              </svg>
            `),
            scaledSize: new window.google.maps.Size(32, 32),
            anchor: new window.google.maps.Point(16, 32),
          },
          zIndex: 1000, // Ensure user marker appears on top
        });

        // Add info window for user location
        const userInfoWindow = new window.google.maps.InfoWindow({
          content: '<div><h4 style="margin: 0; color: #3B82F6;">📍 Your Current Location</h4></div>',
        });

        userMarker.addListener('click', () => {
          userInfoWindow.open(map, userMarker);
        });
      }

      // Sort mandis by distance and add numbering
      let sortedMandis = [...mandis];
      if (userLocation) {
        sortedMandis = mandis.map(mandi => ({
          ...mandi,
          distance: calculateDistance(
            userLocation.lat, userLocation.lng,
            parseFloat(mandi.latitude), parseFloat(mandi.longitude)
          )
        })).sort((a, b) => a.distance - b.distance);
      }

      // Add markers for mandis with distance-based numbering
      sortedMandis.forEach((mandi, index) => {
        const mandiMarker = new window.google.maps.Marker({
          position: { lat: parseFloat(mandi.latitude), lng: parseFloat(mandi.longitude) },
          map: map,
          title: mandi.name,
          icon: {
            url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" fill="${index === 0 ? '#10B981' : '#DC2626'}" stroke="white" stroke-width="2"/>
              </svg>
            `),
            scaledSize: new window.google.maps.Size(28, 28),
            anchor: new window.google.maps.Point(14, 28),
          },
          label: {
            text: (index + 1).toString(),
            color: 'white',
            fontSize: '12px',
            fontWeight: 'bold',
          },
        });

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div style="max-width: 250px;">
              <h3 style="margin: 0 0 8px 0; color: ${index === 0 ? '#10B981' : '#DC2626'}; font-size: 16px;">${index === 0 ? '⭐ ' : ''}${mandi.name}</h3>
              ${userLocation ? `<p style="margin: 4px 0; color: #10B981; font-weight: bold;">📏 Distance: ${(mandi.distance / 1000).toFixed(1)} km</p>` : ''}
              <p style="margin: 4px 0;"><strong>📍 Address:</strong> ${mandi.address}</p>
              <p style="margin: 4px 0;"><strong>📞 Contact:</strong> ${mandi.contact_number}</p>
              <p style="margin: 4px 0;"><strong>🕒 Hours:</strong> ${mandi.operating_hours}</p>
              <p style="margin: 4px 0;"><strong>🏢 Facilities:</strong> ${mandi.facilities ? mandi.facilities.join(', ') : 'Not specified'}</p>
              <button onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${mandi.latitude},${mandi.longitude}', '_blank')"
                      style="background: #3B82F6; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; margin-top: 8px;">
                🗺️ Get Directions
              </button>
            </div>
          `,
        });

        mandiMarker.addListener('click', () => {
          infoWindow.open(map, mandiMarker);
        });
      });
    }
  }, [mandis, userLocation, hasApiKey]);

  // Enhanced fallback map using OpenStreetMap (no API key required)
  if (!hasApiKey) {
    return (
      <div className="w-full h-full">
        <MapContainer
          center={userLocation ? [userLocation.lat, userLocation.lng] : [20.5937, 78.9629]}
          zoom={userLocation ? 10 : 5}
          style={{ height: '100%', width: '100%' }}
          className="rounded-lg"
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />

          {/* User location marker */}
          {userLocation && (
            <Marker
              position={[userLocation.lat, userLocation.lng]}
              icon={L.divIcon({
                html: `
                  <div style="
                    background-color: #3B82F6;
                    border: 3px solid white;
                    border-radius: 50%;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                  ">
                    <div style="
                      background-color: white;
                      border-radius: 50%;
                      width: 8px;
                      height: 8px;
                    "></div>
                  </div>
                `,
                className: 'custom-user-marker',
                iconSize: [24, 24],
                iconAnchor: [12, 12],
              })}
            >
              <Popup>
                <div className="text-center">
                  <h4 className="font-semibold text-blue-600">📍 Your Location</h4>
                  <p className="text-sm text-gray-600">
                    Lat: {userLocation.lat.toFixed(4)}<br/>
                    Lng: {userLocation.lng.toFixed(4)}
                  </p>
                </div>
              </Popup>
            </Marker>
          )}

          {/* Mandi markers - sorted by distance */}
          {(() => {
            let sortedMandis = [...(mandis || [])];
            if (userLocation) {
              sortedMandis = mandis.map(mandi => ({
                ...mandi,
                distance: calculateDistance(
                  userLocation.lat, userLocation.lng,
                  parseFloat(mandi.latitude), parseFloat(mandi.longitude)
                )
              })).sort((a, b) => a.distance - b.distance);
            }
  
            return sortedMandis.map((mandi, index) => (
              <Marker
                key={index}
                position={[parseFloat(mandi.latitude), parseFloat(mandi.longitude)]}
                icon={L.divIcon({
                  html: `
                    <div style="
                      background-color: ${index === 0 ? '#10B981' : '#DC2626'};
                      color: white;
                      border: 2px solid white;
                      border-radius: 50%;
                      width: 28px;
                      height: 28px;
                      display: flex;
                      align-items: center;
                      justify-content: center;
                      font-size: 12px;
                      font-weight: bold;
                      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    ">
                      ${index + 1}
                    </div>
                  `,
                  className: 'custom-mandi-marker',
                  iconSize: [28, 28],
                  iconAnchor: [14, 14],
                })}
              >
                <Popup>
                  <div className="max-w-xs">
                    <h4 className="font-semibold text-gray-800 mb-2">
                      {index === 0 ? '⭐ ' : ''}{mandi.name}
                    </h4>
                    {userLocation && (
                      <p className="text-sm text-green-600 font-medium mb-2">
                        📏 Distance: {(mandi.distance / 1000).toFixed(1)} km
                      </p>
                    )}
                    <p className="text-sm text-gray-600 mb-1">📍 {mandi.address}</p>
                    <p className="text-sm text-gray-600 mb-1">📞 {mandi.contact_number}</p>
                    <p className="text-sm text-gray-600 mb-2">🕒 {mandi.operating_hours}</p>
                    {mandi.facilities && mandi.facilities.length > 0 && (
                      <div className="mb-2">
                        <p className="text-sm font-medium text-gray-700">🏢 Facilities:</p>
                        <p className="text-xs text-gray-600">{mandi.facilities.join(', ')}</p>
                      </div>
                    )}
                    <div className="flex gap-2 mt-3">
                      <button
                        onClick={() => window.open(`https://www.google.com/maps/dir/?api=1&destination=${mandi.latitude},${mandi.longitude}`, '_blank')}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-xs hover:bg-blue-700 transition-colors"
                      >
                        🗺️ Directions
                      </button>
                      <button
                        onClick={() => window.open(`tel:${mandi.contact_number}`, '_self')}
                        className="bg-green-600 text-white px-3 py-1 rounded text-xs hover:bg-green-700 transition-colors"
                      >
                        📞 Call
                      </button>
                    </div>
                  </div>
                </Popup>
              </Marker>
            ));
          })()}
        </MapContainer>
      </div>
    );
  }

  return <div id="marketplace-map" className="w-full h-full rounded-lg"></div>;
};

// OpenStreetMap Component (No API key required)
const OpenStreetMapComponent = ({ mandis, userLocation }) => {
  return (
    <div className="w-full h-full">
      <MapContainer
        center={userLocation ? [userLocation.lat, userLocation.lng] : [20.5937, 78.9629]}
        zoom={userLocation ? 10 : 5}
        style={{ height: '100%', width: '100%' }}
        className="rounded-lg"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {/* User location marker */}
        {userLocation && (
          <Marker
            position={[userLocation.lat, userLocation.lng]}
            icon={L.divIcon({
              html: `
                <div style="
                  background-color: #3B82F6;
                  border: 3px solid white;
                  border-radius: 50%;
                  width: 24px;
                  height: 24px;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                ">
                  <div style="
                    background-color: white;
                    border-radius: 50%;
                    width: 8px;
                    height: 8px;
                  "></div>
                </div>
              `,
              className: 'custom-user-marker',
              iconSize: [24, 24],
              iconAnchor: [12, 12],
            })}
          >
            <Popup>
              <div className="text-center">
                <h4 className="font-semibold text-blue-600">📍 Your Location</h4>
                <p className="text-sm text-gray-600">
                  Lat: {userLocation.lat.toFixed(4)}<br/>
                  Lng: {userLocation.lng.toFixed(4)}
                </p>
              </div>
            </Popup>
          </Marker>
        )}

        {/* Mandi markers - sorted by distance */}
        {(() => {
          let sortedMandis = [...(mandis || [])];
          if (userLocation) {
            sortedMandis = mandis.map(mandi => ({
              ...mandi,
              distance: calculateDistance(
                userLocation.lat, userLocation.lng,
                parseFloat(mandi.latitude), parseFloat(mandi.longitude)
              )
            })).sort((a, b) => a.distance - b.distance);
          }

          return sortedMandis.map((mandi, index) => (
            <Marker
              key={index}
              position={[parseFloat(mandi.latitude), parseFloat(mandi.longitude)]}
              icon={L.divIcon({
                html: `
                  <div style="
                    background-color: ${index === 0 ? '#10B981' : '#DC2626'};
                    color: white;
                    border: 2px solid white;
                    border-radius: 50%;
                    width: 28px;
                    height: 28px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: bold;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                  ">
                    ${index + 1}
                  </div>
                `,
                className: 'custom-mandi-marker',
                iconSize: [28, 28],
                iconAnchor: [14, 14],
              })}
            >
              <Popup>
                <div className="max-w-xs">
                  <h4 className="font-semibold text-gray-800 mb-2">
                    {index === 0 ? '⭐ ' : ''}{mandi.name}
                  </h4>
                  {userLocation && (
                    <p className="text-sm text-green-600 font-medium mb-2">
                      📏 Distance: {(mandi.distance / 1000).toFixed(1)} km
                    </p>
                  )}
                  <p className="text-sm text-gray-600 mb-1">📍 {mandi.address}</p>
                  <p className="text-sm text-gray-600 mb-1">📞 {mandi.contact_number}</p>
                  <p className="text-sm text-gray-600 mb-2">🕒 {mandi.operating_hours}</p>
                  {mandi.facilities && mandi.facilities.length > 0 && (
                    <div className="mb-2">
                      <p className="text-sm font-medium text-gray-700">🏢 Facilities:</p>
                      <p className="text-xs text-gray-600">{mandi.facilities.join(', ')}</p>
                    </div>
                  )}
                  <div className="flex gap-2 mt-3">
                    <button
                      onClick={() => window.open(`https://www.google.com/maps/dir/?api=1&destination=${mandi.latitude},${mandi.longitude}`, '_blank')}
                      className="bg-blue-600 text-white px-3 py-1 rounded text-xs hover:bg-blue-700 transition-colors"
                    >
                      🗺️ Directions
                    </button>
                    <button
                      onClick={() => window.open(`tel:${mandi.contact_number}`, '_self')}
                      className="bg-green-600 text-white px-3 py-1 rounded text-xs hover:bg-green-700 transition-colors"
                    >
                      📞 Call
                    </button>
                  </div>
                </div>
              </Popup>
            </Marker>
          ));
        })()}
      </MapContainer>
    </div>
  );
};

// Mandi Detail Map Component
const MandiDetailMap = ({ mandi, userLocation }) => {
  const hasApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY && import.meta.env.VITE_GOOGLE_MAPS_API_KEY !== "DEMO_KEY";

  useEffect(() => {
    if (hasApiKey && window.google && mandi) {
      const map = new window.google.maps.Map(document.getElementById('mandi-detail-map'), {
        center: { lat: parseFloat(mandi.latitude), lng: parseFloat(mandi.longitude) },
        zoom: 15,
      });

      // Add mandi marker
      const mandiMarker = new window.google.maps.Marker({
        position: { lat: parseFloat(mandi.latitude), lng: parseFloat(mandi.longitude) },
        map: map,
        title: mandi.name,
        icon: {
          url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" fill="#DC2626" stroke="white" stroke-width="2"/>
            </svg>
          `),
          scaledSize: new window.google.maps.Size(32, 32),
        },
      });

      // Add info window
      const infoWindow = new window.google.maps.InfoWindow({
        content: `
          <div style="max-width: 200px;">
            <h3 style="font-weight: bold; margin-bottom: 8px;">${mandi.name}</h3>
            <p style="margin-bottom: 4px;">${mandi.address}</p>
            <p style="margin-bottom: 4px;">📞 ${mandi.contact_number}</p>
            <p style="margin-bottom: 4px;">🕒 ${mandi.operating_hours}</p>
          </div>
        `,
      });

      mandiMarker.addListener('click', () => {
        infoWindow.open(map, mandiMarker);
      });

      // Add user location marker if available
      if (userLocation) {
        new window.google.maps.Marker({
          position: userLocation,
          map: map,
          title: 'Your Location',
          icon: {
            url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" fill="#3B82F6" stroke="white" stroke-width="2"/>
                <circle cx="12" cy="12" r="4" fill="white"/>
              </svg>
            `),
            scaledSize: new window.google.maps.Size(24, 24),
          },
        });

        // Add directions link
        const directionsService = new window.google.maps.DirectionsService();
        const directionsRenderer = new window.google.maps.DirectionsRenderer({
          map: map,
          suppressMarkers: true,
        });

        const request = {
          origin: userLocation,
          destination: { lat: parseFloat(mandi.latitude), lng: parseFloat(mandi.longitude) },
          travelMode: window.google.maps.TravelMode.DRIVING,
        };

        directionsService.route(request, (result, status) => {
          if (status === window.google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(result);
          }
        });
      }
    }
  }, [mandi, userLocation, hasApiKey]);

  if (!hasApiKey) {
    return (
      <div className="w-full h-full bg-gray-100 rounded-lg flex items-center justify-center">
        <div className="text-center p-6">
          <div className="text-4xl mb-4">📍</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">{mandi.name}</h3>
          <p className="text-gray-600 mb-2">{mandi.address}</p>
          <p className="text-sm text-gray-500">📍 {mandi.latitude}, {mandi.longitude}</p>
          <p className="text-sm text-gray-500">📞 {mandi.contact_number}</p>
          <p className="text-sm text-gray-500">🕒 {mandi.operating_hours}</p>
        </div>
      </div>
    );
  }

  return <div id="mandi-detail-map" className="w-full h-full rounded-lg"></div>;
};

export default Marketplace;