export interface MarkerMaster {
  id: number
  name: string
  filePath: string
  category: 'REGISTER' | 'SEARCH' | 'FUNCTION' | 'OTHER'
  isVisible: boolean
  displayOrder: number
  memo: string
  published_at: number
  functionType?: string
  paramJson?: string
  isUnlocked: boolean
  searchKeyword?: string
  description: string
  is_deleted: boolean
}

export interface NotificationMaster {
  id: string
  title: string
  message: string
  scheduled_at: number
  is_push: boolean
  isUserVisible: boolean
  created_at: number
  is_deleted: boolean
}

export interface User {
  id: string
  username: string
  email?: string
  emailVerified: boolean
  fcm_token?: string
  is_registered: boolean
  created_at: number
  updated_at: number
  user_type: string
  is_deleted: boolean
}

export interface FCMNotificationRequest {
  title: string
  message: string
  user_ids?: string[]
  data?: Record<string, any>
}
