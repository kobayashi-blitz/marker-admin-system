import { defineStore } from 'pinia'
import { ref } from 'vue'
import { 
  getAuth, 
  signInWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  type User 
} from 'firebase/auth'
import { initializeApp } from 'firebase/app'
import axios from 'axios'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
}

const app = initializeApp(firebaseConfig)
const auth = getAuth(app)

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = ref(false)

  const login = async (email: string, password: string) => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      user.value = userCredential.user
      token.value = await userCredential.user.getIdToken()
      isAuthenticated.value = true
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  }

  const logout = async () => {
    try {
      await signOut(auth)
      user.value = null
      token.value = null
      isAuthenticated.value = false
      
      delete axios.defaults.headers.common['Authorization']
      
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  }

  const initAuth = () => {
    onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        user.value = firebaseUser
        token.value = await firebaseUser.getIdToken()
        isAuthenticated.value = true
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      } else {
        user.value = null
        token.value = null
        isAuthenticated.value = false
        delete axios.defaults.headers.common['Authorization']
      }
    })
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    initAuth
  }
})
