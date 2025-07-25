<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn icon @click="toggleDrawer">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-app-bar-title>ナカマーカー管理システム</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn @click="logout" variant="text">
        <v-icon>mdi-logout</v-icon>
        ログアウト
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer
      app
      v-model="drawerOpen"
      :mini-variant="!drawerOpen"
      permanent
    >
      <v-list>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.route"
          :prepend-icon="item.icon"
          :title="drawerOpen ? item.title : ''"
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

const drawerOpen = ref(false) // デフォルトで閉じておく

const toggleDrawer = () => {
  drawerOpen.value = !drawerOpen.value
}

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>
