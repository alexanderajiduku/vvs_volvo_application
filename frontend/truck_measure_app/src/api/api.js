import axios from 'axios';
import { BASE_URL } from '../config/config';


/**
 * AuthApi object for handling authentication-related API calls.
 * @typedef {Object} AuthApi
 * @property {Function} signup - Registers a new user.
 * @property {Function} signin - Authenticates a user.
 * @property {Function} getCurrentUser - Function to get the current user.
 * @property {Function} uploadImage - Uploads an image.
 * @property {Function} registerCamera - Registers a camera.
 * @property {Function} getAllCameras - Retrieves all cameras.
 * @property {Function} uploadModel - Uploads a model.
 * @property {Function} getAllModels - Retrieves all models.
 * @property {Function} getModelPath - Retrieves the path of a specific model.
 */


const AuthApi = {
  getAuthToken: () => localStorage.getItem('authToken'),
  setAuthToken: (token) => localStorage.setItem('authToken', token),
  clearAuthToken: () => localStorage.removeItem('authToken'),


  signup: async (formData) => {
    try {
      const response = await axios.post(`${BASE_URL}/api/v1/signup`, formData);
      return { success: true, user: response.data };

    } catch (error) {
      console.error('Signup error:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred. Please try again."];
      return { success: false, errors };
    }
  },
  signin: async (formData) => {
    try {
      const response = await axios.post(`${BASE_URL}/api/v1/signin`, formData);
      const { access_token } = response.data;

      if (access_token) {
        AuthApi.setAuthToken(access_token);
        return { success: true, user: response.data };
      } else {
        console.error('SignIn failed: Invalid response from server', response);
        return { success: false, errors: ["Invalid response from server."] };
      }
    } catch (error) {
      console.error('Login error:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred. Please try again."];
      return { success: false, errors };
    }
  },


  uploadImage: async (imageFile, authToken) => {
    const formData = new FormData();
    formData.append('file', imageFile);

    try {
      const response = await axios.post(`${BASE_URL}/api/v1/uploadimages`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${AuthApi.getAuthToken()}`
        }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Image upload error:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred during image upload. Please try again."];
      return { success: false, errors };
    }
  },
  registerCamera: async (cameraData) => {
    const formData = new FormData();
    for (const key in cameraData) {
      if (cameraData.hasOwnProperty(key)) {
        formData.append(key, cameraData[key]);
      }
    }
    try {
      const response = await axios.post(`${BASE_URL}/api/v1/registercamera`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${AuthApi.getAuthToken()}`
        }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Camera registration error:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred during camera registration. Please try again."];
      return { success: false, errors };
    }
  },
  getAllCameras: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/api/v1/camera`, {
        headers: {
          'Authorization': `Bearer ${AuthApi.getAuthToken()}`
        }
      });
      return { success: true, cameras: response.data };
    } catch (error) {
      console.error('Error fetching cameras:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred while fetching cameras. Please try again."];
      return { success: false, errors };
    }
  },

  // Add this method to AuthApi
  deleteCamera: async (cameraId) => {
    try {
      const response = await axios.delete(`${BASE_URL}/api/v1/camera/${cameraId}`, {
        headers: {
          'Authorization': `Bearer ${AuthApi.getAuthToken()}`
        }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error deleting camera:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred while deleting the camera. Please try again."];
      return { success: false, errors };
    }
  }
  ,

  uploadModel: async (formData) => {
    try {
      const response = await axios.post(`${BASE_URL}/api/v1/model`, formData, {
        headers: {
          'Authorization': `Bearer ${AuthApi.getAuthToken()}`
        }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Model upload error:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred during model upload. Please try again."];
      return { success: false, errors };
    }
  },

  getAllModels: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/api/v1/model`, {
        headers: {
          'Authorization': `Bearer ${AuthApi.getAuthToken()}`
        }
      });
      return { success: true, models: response.data };
    } catch (error) {
      console.error('Error fetching models:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred while fetching models. Please try again."];
      return { success: false, errors };
    }
  },

  getModelPath: async (model_id) => {
    try {
      const response = await axios.post(`${BASE_URL}/api/v1/model/${model_id}/path`, {
        headers: {
          'Authorization': `Bearer ${AuthApi.getAuthToken()}`
        }
      });
      return { success: true, model_path: response.data.model_path };
    } catch (error) {
      console.error('Error fetching model path:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred while fetching model path. Please try again."];
      return { success: false, errors };
    }
  },

  deleteModel: async (modelId) => {
    try {
      const response = await axios.delete(`${BASE_URL}/api/v1/model/${modelId}`, {
        headers: {
          'Authorization': `Bearer ${AuthApi.getAuthToken()}`
        }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error deleting model:', error.response || error);
      const errors = error.response?.data?.detail || ["An unexpected error occurred while deleting the model. Please try again."];
      return { success: false, errors };
    }
  },
};

export default AuthApi;
