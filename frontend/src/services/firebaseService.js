import { database, storage, auth } from '../firebase'
import { ref, set, get, remove, update } from 'firebase/database'
import { ref as storageRef, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage'

// Database operations
export const saveChat = async (chatId, chatData) => {
  try {
    const dbRef = ref(database, `chats/${chatId}`)
    await set(dbRef, { ...chatData, createdAt: new Date().toISOString() })
    return { success: true, chatId }
  } catch (error) {
    console.error('Error saving chat:', error)
    return { success: false, error: error.message }
  }
}

export const getChat = async (chatId) => {
  try {
    const dbRef = ref(database, `chats/${chatId}`)
    const snapshot = await get(dbRef)
    if (snapshot.exists()) {
      return { success: true, data: snapshot.val() }
    } else {
      return { success: false, error: 'Chat not found' }
    }
  } catch (error) {
    console.error('Error getting chat:', error)
    return { success: false, error: error.message }
  }
}

export const getAllChats = async () => {
  try {
    const dbRef = ref(database, 'chats')
    const snapshot = await get(dbRef)
    if (snapshot.exists()) {
      const chats = []
      snapshot.forEach(child => {
        chats.push({ id: child.key, ...child.val() })
      })
      return { success: true, data: chats }
    } else {
      return { success: true, data: [] }
    }
  } catch (error) {
    console.error('Error getting chats:', error)
    return { success: false, error: error.message }
  }
}

export const deleteChat = async (chatId) => {
  try {
    const dbRef = ref(database, `chats/${chatId}`)
    await remove(dbRef)
    return { success: true }
  } catch (error) {
    console.error('Error deleting chat:', error)
    return { success: false, error: error.message }
  }
}

export const updateChat = async (chatId, updates) => {
  try {
    const dbRef = ref(database, `chats/${chatId}`)
    await update(dbRef, updates)
    return { success: true }
  } catch (error) {
    console.error('Error updating chat:', error)
    return { success: false, error: error.message }
  }
}

// Storage operations
export const uploadAudio = async (file, path) => {
  try {
    const fileRef = storageRef(storage, path)
    const snapshot = await uploadBytes(fileRef, file)
    const downloadURL = await getDownloadURL(snapshot.ref)
    return { success: true, url: downloadURL }
  } catch (error) {
    console.error('Error uploading audio:', error)
    return { success: false, error: error.message }
  }
}

export const uploadFile = async (file, path) => {
  try {
    const fileRef = storageRef(storage, path)
    const snapshot = await uploadBytes(fileRef, file)
    const downloadURL = await getDownloadURL(snapshot.ref)
    return { success: true, url: downloadURL }
  } catch (error) {
    console.error('Error uploading file:', error)
    return { success: false, error: error.message }
  }
}

export const deleteFile = async (path) => {
  try {
    const fileRef = storageRef(storage, path)
    await deleteObject(fileRef)
    return { success: true }
  } catch (error) {
    console.error('Error deleting file:', error)
    return { success: false, error: error.message }
  }
}

// User operations
export const saveUserData = async (userId, userData) => {
  try {
    const dbRef = ref(database, `users/${userId}`)
    await set(dbRef, { ...userData, updatedAt: new Date().toISOString() })
    return { success: true }
  } catch (error) {
    console.error('Error saving user data:', error)
    return { success: false, error: error.message }
  }
}

export const getUserData = async (userId) => {
  try {
    const dbRef = ref(database, `users/${userId}`)
    const snapshot = await get(dbRef)
    if (snapshot.exists()) {
      return { success: true, data: snapshot.val() }
    } else {
      return { success: true, data: null }
    }
  } catch (error) {
    console.error('Error getting user data:', error)
    return { success: false, error: error.message }
  }
}
