import { initializeApp } from 'firebase/app'
import { getDatabase } from 'firebase/database'
import { getStorage } from 'firebase/storage'
import { getAuth } from 'firebase/auth'

// Your Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDp3kratwmZpLK5_gVo-tq2Wmi90DXsLlk",
  authDomain: "thevibemarket-f3ac5.firebaseapp.com",
  databaseURL: "https://thevibemarket-f3ac5-default-rtdb.firebaseio.com",
  projectId: "thevibemarket-f3ac5",
  storageBucket: "thevibemarket-f3ac5.firebasestorage.app",
  messagingSenderId: "289448937056",
  appId: "1:289448937056:web:738e19cb4cdba86e136505",
  measurementId: "G-G4J170V5JQ"
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)

// Get Firebase services
const database = getDatabase(app)
const storage = getStorage(app)
const auth = getAuth(app)

export { app, database, storage, auth }
