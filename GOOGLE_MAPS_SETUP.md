# Google Maps Integration Setup

## Issue: "Oops! Something went wrong. This page didn't load Google Maps correctly."

This error occurs because the Google Maps integration requires a valid API key. Here's how to fix it:

## Step 1: Get a Google Maps API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Geocoding API** (optional, for address search)
4. Create credentials (API Key)
5. Restrict the API key to your domain for security (recommended)

## Step 2: Configure the API Key

1. In the `frontend` directory, create a `.env` file:
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API key:
   ```env
   VITE_GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```

## Step 3: Restart the Development Server

After adding the API key, restart the frontend development server:

```bash
cd frontend
npm run dev
```

## Features Available with Google Maps API Key

✅ **Interactive Map**: Clickable markers showing mandi locations
✅ **User Location**: Automatic detection and display of your location
✅ **Info Windows**: Detailed information when clicking on markers
✅ **Zoom & Pan**: Full map navigation controls
✅ **Distance Calculation**: Proximity to nearest mandis

## Without API Key (Current Fallback)

The application includes a fallback that displays:
- Static list of mandi locations
- Basic location information
- Contact details
- Coordinates

## Troubleshooting

### Common Issues:

1. **API Key Not Recognized**: Make sure the `.env` file is in the `frontend` directory
2. **API Not Enabled**: Ensure Maps JavaScript API is enabled in Google Cloud Console
3. **Domain Restrictions**: If you set domain restrictions, make sure `localhost:5174` is allowed
4. **Billing**: Google Maps requires billing to be enabled for production use

### Test the API Key

You can test if your API key is working by visiting:
```
https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap
```

## Security Note

- Never commit your `.env` file to version control
- Restrict your API key to specific domains in production
- Monitor your API usage in Google Cloud Console

## Cost Information

Google Maps API has a free tier:
- $200 credit per month
- 28,000 map loads per month free
- Additional usage is billed per request

For more information, visit: https://developers.google.com/maps/billing-and-pricing/pricing