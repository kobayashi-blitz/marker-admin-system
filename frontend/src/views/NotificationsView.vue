<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1>通知マスタ</h1>
      </v-col>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { notificationApi } from '../services/api'
import type { NotificationMaster } from '../types'

const notifications = ref<NotificationMaster[]>([])
const loading = ref(false)

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'タイトル', key: 'title' },
  { title: 'メッセージ', key: 'message' },
  { title: 'プッシュ', key: 'is_push' },
  { title: '表示', key: 'isUserVisible' },
  { title: 'アクション', key: 'actions', sortable: false }
]

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
  console.log('Create dialog')
}

const editItem = (item: NotificationMaster) => {
  console.log('Edit item:', item)
}

const deleteItem = (item: NotificationMaster) => {
  console.log('Delete item:', item)
}

onMounted(() => {
  fetchNotifications()
})
</script>
