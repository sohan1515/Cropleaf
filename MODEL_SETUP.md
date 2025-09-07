# CropLeaf ML Model Setup Guide

This guide explains how to set up your ML models for deployment after removing them from Git tracking.

## 🚀 Quick Start

1. **Upload models to cloud storage**
2. **Configure environment variables**
3. **Deploy your application**

## 📁 Model Files

Your application uses two ML model files:
- `CropLeaf-C1.h5` - TensorFlow/Keras model (170MB)
- `plant_disease_model_1_latest.pt` - PyTorch model (210MB)

## 🗂️ Storage Options

### Option 1: Google Drive (Recommended)

1. **Upload your model files to Google Drive**
   - Go to [Google Drive](https://drive.google.com)
   - Upload `CropLeaf-C1.h5` and `plant_disease_model_1_latest.pt`

2. **Make files publicly accessible**
   - Right-click each file → "Get shareable link"
   - Set permissions to "Anyone with the link can view"
   - Copy the file ID from the share link

   Example share link: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
   The FILE_ID is the part between `/d/` and `/view`

3. **Configure environment variables**
   ```bash
   TF_MODEL_GOOGLE_DRIVE_ID=your_tensorflow_file_id_here
   PT_MODEL_GOOGLE_DRIVE_ID=your_pytorch_file_id_here
   ```

### Option 2: Direct URL Download

1. **Upload to any cloud storage**
   - AWS S3, Dropbox, GitHub Releases, etc.
   - Make files publicly accessible

2. **Configure environment variables**
   ```bash
   TF_MODEL_URL=https://example.com/path/to/CropLeaf-C1.h5
   PT_MODEL_URL=https://example.com/path/to/plant_disease_model_1_latest.pt
   ```

## ⚙️ Environment Configuration

### For Railway Deployment

1. **Go to your Railway project dashboard**
2. **Navigate to Variables section**
3. **Add the following variables:**

```bash
# Choose ONE method per model
TF_MODEL_GOOGLE_DRIVE_ID=1ABC...xyz  # OR
TF_MODEL_URL=https://example.com/CropLeaf-C1.h5

PT_MODEL_GOOGLE_DRIVE_ID=2DEF...uvw  # OR
PT_MODEL_URL=https://example.com/plant_disease_model_1_latest.pt
```

### For Other Platforms

- **Heroku**: Set config vars in dashboard
- **Render**: Set environment variables in dashboard
- **Vercel**: Set environment variables in project settings
- **Local development**: Create `.env` file in backend directory

## 🔧 Manual Model Download

If you need to download models manually:

```bash
cd backend
python download_models.py
```

This script will:
- Check for configured download URLs
- Download missing models
- Verify successful downloads

## 🧪 Testing Model Loading

### Local Testing

1. **Set environment variables** in `.env` file
2. **Run the download script**:
   ```bash
   python download_models.py
   ```
3. **Start Django server**:
   ```bash
   python manage.py runserver
   ```
4. **Test model prediction** by uploading an image

### Deployment Testing

1. **Deploy your application**
2. **Check deployment logs** for model download messages
3. **Test image upload functionality**
4. **Verify predictions are working**

## 📋 Troubleshooting

### Common Issues

**Models not downloading during deployment:**
- Check environment variables are set correctly
- Verify file permissions on cloud storage
- Check deployment logs for error messages

**Model loading errors:**
- Ensure model files are not corrupted
- Check file paths in `model.py`
- Verify TensorFlow/PyTorch versions match training environment

**Large file upload timeouts:**
- Use Google Drive for more reliable downloads
- Consider compressing models if possible
- Increase timeout values in download script

### Debug Commands

```bash
# Check if models exist
ls -la backend/app/ml_models/

# Test model loading manually
cd backend
python -c "from app.model import model; print(f'Model type: {model.model_type}')"

# Check environment variables
echo $TF_MODEL_GOOGLE_DRIVE_ID
echo $PT_MODEL_GOOGLE_DRIVE_ID
```

## 🔒 Security Considerations

- **Keep model files secure**: Only share download links publicly if necessary
- **Use HTTPS URLs**: Ensure download URLs use HTTPS
- **Monitor access**: Check cloud storage access logs
- **Regular updates**: Update model files and access tokens periodically

## 📞 Support

If you encounter issues:
1. Check the deployment logs
2. Verify environment variable configuration
3. Test model downloads locally first
4. Ensure cloud storage permissions are correct

## 🎯 Best Practices

- **Use Google Drive** for reliability and ease of use
- **Test locally first** before deploying
- **Monitor download times** for large files
- **Keep backup copies** of your models
- **Document your setup** for team members

---

**Note**: This setup ensures your repository remains lightweight while making models available for deployment. The models are downloaded automatically during the deployment process.