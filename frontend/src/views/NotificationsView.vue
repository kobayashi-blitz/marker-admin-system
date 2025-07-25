<template>
  <div>
    <v-row class="mb-4">
      
      <v-col cols="auto">
        <v-btn color="primary" @click="openCreateDialog">
          <v-icon left>mdi-plus</v-icon>
          新規登録
        </v-btn>
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="notifications"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.scheduled_at="{ item }">
        <span>
          {{ formatDate(item.scheduled_at) }}
        </span>
      </template>

      <template v-slot:item.is_push="{ item }">
        <v-chip :color="item.is_push ? 'success' : 'error'">
          {{ item.is_push ? 'プッシュ通知' : '通常通知' }}
        </v-chip>
      </template>
      
      <template v-slot:item.isUserVisible="{ item }">
        <v-chip :color="item.isUserVisible ? 'success' : 'error'">
          {{ item.isUserVisible ? '表示' : '非表示' }}
        </v-chip>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
          @click="editItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          small
          @click="deleteItem(item)"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editedIndex === -1 ? '新規通知作成' : '通知編集' }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" v-if="editedIndex !== -1">
                <v-text-field
                  v-model="editedItem.id"
                  label="通知ID"
                  readonly
                  variant="underlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.title"
                  label="タイトル*"
                  required
                  :error-messages="titleErrors"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.message"
                  label="メッセージ*"
                  required
                  :error-messages="messageErrors"
                ></v-textarea>
              </v-col>
              <v-col cols="12" sm="6">
                <v-switch
                  v-model="editedItem.is_push"
                  label="プッシュ通知"
                  :color="editedItem.is_push ? 'success' : 'error'"
                ></v-switch>
              </v-col>
              <v-col cols="12" sm="6">
                <v-switch
                  v-model="editedItem.isUserVisible"
                  label="ユーザーに表示"
                  :color="editedItem.isUserVisible ? 'success' : 'error'"
                ></v-switch>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="scheduledDateString"
                  label="配信予定日時*"
                  type="datetime-local"
                  required
                  :error-messages="dateErrors"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close">
            キャンセル
          </v-btn>
          <v-btn color="blue darken-1" text @click="save" :loading="saving">
            保存
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">削除確認</v-card-title>
        <v-card-text>この通知を削除してもよろしいですか？</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDelete">キャンセル</v-btn>
          <v-btn color="red darken-1" text @click="deleteItemConfirm" :loading="deleting">削除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { notificationApi } from '../services/api'
import type { NotificationMaster } from '../types'

const notifications = ref<NotificationMaster[]>([])
const loading = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editedIndex = ref(-1)
const editedItem = ref<Partial<NotificationMaster>>({})
const itemToDelete = ref<NotificationMaster | null>(null)
const scheduledDateString = ref('')

const headers = [
  { title: 'タイトル', key: 'title' },
  { title: 'メッセージ', key: 'message' },
  { title: '配信予定日', key: 'scheduled_at' },
  { title: 'プッシュ', key: 'is_push' },
  { title: '表示', key: 'isUserVisible' },
  { title: 'アクション', key: 'actions', sortable: false }
]

function formatDate(timestamp: number) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const defaultItem: Partial<NotificationMaster> = {
  title: '',
  message: '',
  is_push: true,
  isUserVisible: true
}

const titleErrors = computed(() => {
  const errors: string[] = []
  if (!editedItem.value.title) errors.push('タイトルは必須です')
  if (editedItem.value.title && editedItem.value.title.length > 100) errors.push('タイトルは100文字以内で入力してください')
  return errors
})

const messageErrors = computed(() => {
  const errors: string[] = []
  if (!editedItem.value.message) errors.push('メッセージは必須です')
  if (editedItem.value.message && editedItem.value.message.length > 500) errors.push('メッセージは500文字以内で入力してください')
  return errors
})

const dateErrors = computed(() => {
  const errors: string[] = []
  if (!scheduledDateString.value) errors.push('配信予定日時は必須です')
  return errors
})

const isFormValid = computed(() => {
  return titleErrors.value.length === 0 && 
         messageErrors.value.length === 0 && 
         dateErrors.value.length === 0
})

watch(dialog, (val) => {
  val || close()
})

watch(deleteDialog, (val) => {
  val || closeDelete()
})

const fetchNotifications = async () => {
  loading.value = true
  try {
    const response = await notificationApi.getAll()
    notifications.value = response.data
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  editedIndex.value = -1
  editedItem.value = { ...defaultItem }
  const now = new Date()
  scheduledDateString.value = now.toISOString().slice(0, 16)
  dialog.value = true
}

const editItem = (item: NotificationMaster) => {
  editedIndex.value = notifications.value.indexOf(item)
  editedItem.value = { ...item }
  const date = new Date(item.scheduled_at)
  scheduledDateString.value = date.toISOString().slice(0, 16)
  dialog.value = true
}

const deleteItem = (item: NotificationMaster) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const close = () => {
  dialog.value = false
  setTimeout(() => {
    editedItem.value = { ...defaultItem }
    editedIndex.value = -1
    scheduledDateString.value = ''
  }, 300)
}

const closeDelete = () => {
  deleteDialog.value = false
  setTimeout(() => {
    itemToDelete.value = null
  }, 300)
}

const save = async () => {
  if (!isFormValid.value) return

  saving.value = true
  try {
    const notificationData = {
      ...editedItem.value,
      scheduled_at: new Date(scheduledDateString.value).getTime(),
      created_at: editedIndex.value === -1 ? Date.now() : editedItem.value.created_at
    }

    if (editedIndex.value > -1) {
      await notificationApi.update(editedItem.value.id!, notificationData)
    } else {
      await notificationApi.create(notificationData)
    }
    
    await fetchNotifications()
    close()
  } catch (error) {
    console.error('Failed to save notification:', error)
  } finally {
    saving.value = false
  }
}

const deleteItemConfirm = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await notificationApi.delete(itemToDelete.value.id)
    await fetchNotifications()
    closeDelete()
  } catch (error) {
    console.error('Failed to delete notification:', error)
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchNotifications()
})
</script>
