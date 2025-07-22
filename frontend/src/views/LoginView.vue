<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>ログイン</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="email"
                label="メールアドレス"
                name="email"
                prepend-icon="mdi-account"
                type="email"
                :rules="emailRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="パスワード"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                :rules="passwordRules"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              :loading="loading"
              @click="handleLogin"
            >
              ログイン
            </v-btn>
          </v-card-actions>
        </v-card>

        <v-alert
          v-if="error"
          type="error"
          class="mt-4"
        >
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const emailRules = [
  (v: string) => !!v || 'メールアドレスは必須です',
  (v: string) => /.+@.+\..+/.test(v) || '有効なメールアドレスを入力してください'
]

const passwordRules = [
  (v: string) => !!v || 'パスワードは必須です',
  (v: string) => v.length >= 6 || 'パスワードは6文字以上で入力してください'
]

const handleLogin = async () => {
  if (!email.value || !password.value) {
    error.value = 'メールアドレスとパスワードを入力してください'
    return
  }

  loading.value = true
  error.value = ''

  const result = await authStore.login(email.value, password.value)
  
  if (result.success) {
    router.push('/markers')
  } else {
    error.value = result.error || 'ログインに失敗しました'
  }

  loading.value = false
}
</script>
