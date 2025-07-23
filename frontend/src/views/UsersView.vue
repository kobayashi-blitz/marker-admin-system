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

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editedIndex === -1 ? '新規ユーザー作成' : 'ユーザー編集' }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.id"
                  label="Firebase UID*"
                  required
                  :disabled="editedIndex !== -1"
                  :error-messages="idErrors"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.username"
                  label="ユーザー名*"
                  required
                  :error-messages="usernameErrors"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.email"
                  label="メールアドレス"
                  type="email"
                  :error-messages="emailErrors"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.fcm_token"
                  label="FCMトークン"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-switch
                  v-model="editedItem.emailVerified"
                  label="メール認証済み"
                ></v-switch>
              </v-col>
              <v-col cols="12" sm="6">
                <v-switch
                  v-model="editedItem.is_registered"
                  label="登録済み"
                ></v-switch>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedItem.user_type"
                  :items="userTypes"
                  label="ユーザータイプ"
                ></v-select>
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
        <v-card-text>このユーザーを削除してもよろしいですか？</v-card-text>
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
import { userApi } from '../services/api'
import type { User } from '../types'

const users = ref<User[]>([])
const loading = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editedIndex = ref(-1)
const editedItem = ref<Partial<User>>({})
const itemToDelete = ref<User | null>(null)

const headers = [
  { title: 'Firebase UID', key: 'id' },
  { title: 'ユーザー名', key: 'username' },
  { title: 'メール', key: 'email' },
  { title: 'メール認証', key: 'emailVerified' },
  { title: '登録状態', key: 'is_registered' },
  { title: 'アクション', key: 'actions', sortable: false }
]

const userTypes = [
  { title: 'ユーザー', value: 'USER' },
  { title: '管理者', value: 'ADMIN' }
]

const defaultItem: Partial<User> = {
  id: '',
  username: '',
  email: '',
  emailVerified: false,
  fcm_token: '',
  is_registered: true,
  user_type: 'USER'
}

const idErrors = computed(() => {
  const errors: string[] = []
  if (!editedItem.value.id) errors.push('Firebase UIDは必須です')
  if (editedItem.value.id && editedItem.value.id.length < 10) errors.push('Firebase UIDは10文字以上で入力してください')
  return errors
})

const usernameErrors = computed(() => {
  const errors: string[] = []
  if (!editedItem.value.username) errors.push('ユーザー名は必須です')
  if (editedItem.value.username && editedItem.value.username.length > 50) errors.push('ユーザー名は50文字以内で入力してください')
  return errors
})

const emailErrors = computed(() => {
  const errors: string[] = []
  if (editedItem.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(editedItem.value.email)) {
    errors.push('有効なメールアドレスを入力してください')
  }
  return errors
})

const isFormValid = computed(() => {
  return idErrors.value.length === 0 && 
         usernameErrors.value.length === 0 && 
         emailErrors.value.length === 0
})

watch(dialog, (val) => {
  val || close()
})

watch(deleteDialog, (val) => {
  val || closeDelete()
})

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
  editedIndex.value = -1
  editedItem.value = { ...defaultItem }
  dialog.value = true
}

const editItem = (item: User) => {
  editedIndex.value = users.value.indexOf(item)
  editedItem.value = { ...item }
  dialog.value = true
}

const deleteItem = (item: User) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const close = () => {
  dialog.value = false
  setTimeout(() => {
    editedItem.value = { ...defaultItem }
    editedIndex.value = -1
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
    const userData = {
      ...editedItem.value,
      created_at: editedIndex.value === -1 ? Date.now() : editedItem.value.created_at,
      updated_at: Date.now()
    }

    if (editedIndex.value > -1) {
      await userApi.update(editedItem.value.id!, userData)
    } else {
      await userApi.create(userData)
    }
    
    await fetchUsers()
    close()
  } catch (error) {
    console.error('Failed to save user:', error)
  } finally {
    saving.value = false
  }
}

const deleteItemConfirm = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await userApi.delete(itemToDelete.value.id)
    await fetchUsers()
    closeDelete()
  } catch (error) {
    console.error('Failed to delete user:', error)
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
