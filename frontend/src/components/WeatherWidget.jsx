import { useState, useEffect } from 'react';
import { getTranslation } from '../translations';

const WeatherWidget = ({ language = 'en', location = null }) => {
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (location) {
      fetchWeatherData();
    }
  }, [location]);

  const fetchWeatherData = async () => {
    try {
      setLoading(true);
      setError('');

      // Get user's location if not provided
      let lat, lon, locationName;
      if (location) {
        lat = location.lat;
        lon = location.lon;
        locationName = location.name;
      } else {
        // Get user's current location
        const position = await getCurrentPosition();
        lat = position.coords.latitude;
        lon = position.coords.longitude;
        locationName = 'Your Location';
      }

      // Fetch current weather
      const weatherResponse = await fetch(
        `http://localhost:8000/api/weather/current/?lat=${lat}&lon=${lon}&location=${encodeURIComponent(locationName)}`,
        { credentials: 'include' }
      );
      const weatherData = await weatherResponse.json();

      // Fetch forecast
      const forecastResponse = await fetch(
        `http://localhost:8000/api/weather/forecast/?lat=${lat}&lon=${lon}&location=${encodeURIComponent(locationName)}&days=5`,
        { credentials: 'include' }
      );
      const forecastData = await forecastResponse.json();

      setWeather(weatherData);
      setForecast(forecastData);
    } catch (err) {
      setError('Failed to load weather data');
      console.error('Weather error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getCurrentPosition = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported'));
        return;
      }

      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 300000 // 5 minutes
      });
    });
  };

  const getWeatherIcon = (iconCode) => {
    return `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
  };

  const getWeatherConditionColor = (condition) => {
    const colors = {
      'Clear': 'text-yellow-500',
      'Clouds': 'text-gray-500',
      'Rain': 'text-blue-500',
      'Snow': 'text-blue-300',
      'Thunderstorm': 'text-purple-600',
      'Drizzle': 'text-blue-400',
      'Mist': 'text-gray-400',
      'Fog': 'text-gray-400'
    };
    return colors[condition] || 'text-gray-500';
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="text-center text-gray-500">
          <p>{error}</p>
          <button
            onClick={fetchWeatherData}
            className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      {/* Current Weather */}
      {weather && (
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              {getTranslation('currentWeather', language) || 'Current Weather'}
            </h3>
            <span className="text-sm text-gray-500">{weather.location}</span>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <img
                src={getWeatherIcon(weather.weather_icon)}
                alt={weather.weather_description}
                className="w-16 h-16 mr-4"
              />
              <div>
                <div className="text-3xl font-bold text-gray-900">
                  {Math.round(weather.temperature)}°C
                </div>
                <div className={`text-sm font-medium ${getWeatherConditionColor(weather.weather_condition)}`}>
                  {weather.weather_description}
                </div>
              </div>
            </div>

            <div className="text-right text-sm text-gray-600">
              <div>💧 {weather.humidity}%</div>
              <div>💨 {weather.wind_speed} m/s</div>
              <div>👁️ {weather.visibility ? `${weather.visibility}m` : 'N/A'}</div>
            </div>
          </div>
        </div>
      )}

      {/* 5-Day Forecast */}
      {forecast && forecast.forecast && (
        <div>
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            {getTranslation('forecast', language) || '5-Day Forecast'}
          </h4>

          <div className="grid grid-cols-5 gap-2">
            {forecast.forecast.slice(0, 5).map((day, index) => (
              <div key={index} className="text-center p-2 bg-gray-50 rounded-lg">
                <div className="text-xs text-gray-500 mb-1">
                  {new Date(day.date).toLocaleDateString(language, { weekday: 'short' })}
                </div>
                <img
                  src={getWeatherIcon(day.weather_icon)}
                  alt={day.weather_description}
                  className="w-8 h-8 mx-auto mb-1"
                />
                <div className="text-sm font-semibold text-gray-900">
                  {Math.round(day.temperature)}°
                </div>
                <div className="text-xs text-gray-500">
                  {day.precipitation_probability > 30 && '🌧️'}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Weather Alerts */}
      {weather && weather.temperature > 35 && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <span className="text-red-500 mr-2">⚠️</span>
            <span className="text-sm text-red-700">
              {getTranslation('heatAlert', language) || 'High temperature alert - Take precautions'}
            </span>
          </div>
        </div>
      )}

      {forecast && forecast.forecast.some(day => day.precipitation_probability > 70) && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center">
            <span className="text-blue-500 mr-2">🌧️</span>
            <span className="text-sm text-blue-700">
              {getTranslation('rainAlert', language) || 'Heavy rain expected - Prepare accordingly'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default WeatherWidget;