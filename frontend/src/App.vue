<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-title>Mapbox Management System</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn @click="logout" variant="text">
        <v-icon>mdi-logout</v-icon>
        ログアウト
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer app permanent>
      <v-list>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.route"
          :prepend-icon="item.icon"
          :title="item.title"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const menuItems = ref([
  {
    title: 'マーカーマスタ',
    icon: 'mdi-map-marker',
    route: '/markers'
  },
  {
    title: '通知マスタ',
    icon: 'mdi-bell',
    route: '/notifications'
  },
  {
    title: 'ユーザー一覧',
    icon: 'mdi-account-group',
    route: '/users'
  }
])

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>
