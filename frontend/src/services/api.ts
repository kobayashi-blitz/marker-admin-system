import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const markerApi = {
  getAll: (skip = 0, limit = 100) => api.get(`/api/markers?skip=${skip}&limit=${limit}`),
  getById: (id: number) => api.get(`/api/markers/${id}`),
  create: (data: any) => api.post('/api/markers', data),
  update: (id: number, data: any) => api.put(`/api/markers/${id}`, data),
  delete: (id: number) => api.delete(`/api/markers/${id}`)
}

export const notificationApi = {
  getAll: (skip = 0, limit = 100) => api.get(`/api/notifications?skip=${skip}&limit=${limit}`),
  getById: (id: string) => api.get(`/api/notifications/${id}`),
  create: (data: any) => api.post('/api/notifications', data),
  update: (id: string, data: any) => api.put(`/api/notifications/${id}`, data),
  delete: (id: string) => api.delete(`/api/notifications/${id}`)
}

export const userApi = {
  getAll: (skip = 0, limit = 100) => api.get(`/api/users?skip=${skip}&limit=${limit}`),
  getById: (id: string) => api.get(`/api/users/${id}`),
  create: (data: any) => api.post('/api/users', data),
  update: (id: string, data: any) => api.put(`/api/users/${id}`, data),
  delete: (id: string) => api.delete(`/api/users/${id}`)
}

export const uploadApi = {
  uploadFile: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}

export const fcmApi = {
  sendNotification: (data: any) => api.post('/api/fcm/send', data)
}

export default api
