import axios from 'axios';
import { File as FileType } from '../types/file';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const fileService = {
  async uploadFile(file: File): Promise<FileType> {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/files/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.data?.detail === "A file with the same content already exists.") {
        const duplicateFile = error.response.data.file; // Extract duplicate file metadata
        throw new Error(
          `Duplicate file detected. File "${duplicateFile.original_filename}" was uploaded on ${new Date(
            duplicateFile.uploaded_at
          ).toLocaleString()}.`
        );
      }
      throw error;
    }
  },

  async getFiles(filters: any): Promise<FileType[]> {
    const params = new URLSearchParams(filters).toString();
    const response = await axios.get(`${API_URL}/files/?${params}`);
    return response.data;
  },

  async deleteFile(id: string): Promise<void> {
    await axios.delete(`${API_URL}/files/${id}/`);
  },

  async downloadFile(fileUrl: string, filename: string): Promise<void> {
    try {
      const response = await axios.get(fileUrl, {
        responseType: 'blob',
      });

      // Create a blob URL and trigger download
      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download error:', error);
      throw new Error('Failed to download file');
    }
  },

  async getStorageSavings(): Promise<number> {
    const response = await axios.get(`${API_URL}/storage-savings/`);
    return response.data.storage_savings;
  },

};

export default fileService;
