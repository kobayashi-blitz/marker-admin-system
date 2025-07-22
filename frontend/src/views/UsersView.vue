<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1>ユーザー一覧</h1>
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
      :items="users"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.emailVerified="{ item }">
        <v-chip :color="item.emailVerified ? 'success' : 'warning'">
          {{ item.emailVerified ? '認証済み' : '未認証' }}
        </v-chip>
      </template>
      
      <template v-slot:item.is_registered="{ item }">
        <v-chip :color="item.is_registered ? 'success' : 'error'">
          {{ item.is_registered ? '登録済み' : '未登録' }}
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
import { userApi } from '../services/api'
import type { User } from '../types'

const users = ref<User[]>([])
const loading = ref(false)

const headers = [
  { title: 'Firebase UID', key: 'id' },
  { title: 'ユーザー名', key: 'username' },
  { title: 'メール', key: 'email' },
  { title: 'メール認証', key: 'emailVerified' },
  { title: '登録状態', key: 'is_registered' },
  { title: 'アクション', key: 'actions', sortable: false }
]

const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await userApi.getAll()
    users.value = response.data
  } catch (error) {
    console.error('Failed to fetch users:', error)
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  console.log('Create dialog')
}

const editItem = (item: User) => {
  console.log('Edit item:', item)
}

const deleteItem = (item: User) => {
  console.log('Delete item:', item)
}

onMounted(() => {
  fetchUsers()
})
</script>
