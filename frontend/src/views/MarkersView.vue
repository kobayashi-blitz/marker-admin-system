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
      :items="markers"
      :loading="loading"
      class="elevation-1"
      :items-per-page="10"
      no-data-text="データがありません"
      item-value="id"
      :sort-by="[{ key: 'published_at', order: 'desc' }]"
    >
      <template v-slot:item.name="{ item }">
        {{ item.name || '-' }}
      </template>

      <template v-slot:item.filePath="{ item }">
        <div class="d-flex justify-center" style="width: 80px;">
          <img 
            v-if="item.filePath && item.filePath.trim() !== ''" 
            :src="getImageUrl(item.filePath)"
            width="50"
            height="50"
            style="object-fit: cover; border-radius: 4px; border: 1px solid #ddd;"
            @error="handleImageError"
            @load="handleImageLoad"
          />
          <span v-else>-</span>
        </div>
      </template>

      <template v-slot:item.category="{ item }">
        {{
          item.category === 'REGISTER' ? '登録' :
          item.category === 'SEARCH' ? '検索' :
          item.category === 'FUNCTION' ? '機能' :
          item.category === 'OTHER' ? 'その他' :
          '-'
        }}
      </template>

      <template v-slot:item.published_at="{ item }">
        {{ formatDate(item.published_at) }}
      </template>

      <template v-slot:item.description="{ item }">
        {{ item.description || '-' }}
      </template>

      <template v-slot:item.isVisible="{ item }">
        <v-chip :color="item.isVisible ? 'success' : 'error'">
          {{ item.isVisible ? '表示' : '非表示' }}
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
          <span class="text-h5">{{ editedIndex === -1 ? '新規マーカー' : 'マーカー編集' }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-form ref="form" v-model="valid">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="editedItem.name"
                    label="名前*"
                    required
                    :rules="[v => !!v || '名前は必須です']"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="editedItem.category"
                    :items="categoryOptions"
                    label="カテゴリ*"
                    required
                    :rules="[v => !!v || 'カテゴリは必須です']"
                  ></v-select>
                </v-col>
                <v-col cols="12">
                  <v-file-input
                    v-model="selectedFile"
                    label="画像ファイル"
                    accept="image/*"
                    prepend-icon="mdi-camera"
                    @change="onFileChange"
                    clearable
                  ></v-file-input>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.published_at"
                    label="配信日"
                    type="datetime-local"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                    v-model="editedItem.description"
                    label="説明*"
                    required
                    :rules="[v => !!v || '説明は必須です']"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-form>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" variant="text" @click="close">
            キャンセル
          </v-btn>
          <v-btn color="blue darken-1" variant="text" @click="save" :loading="saving">
            保存
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">削除確認</v-card-title>
        <v-card-text>このマーカーを削除してもよろしいですか？</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" variant="text" @click="deleteDialog = false">キャンセル</v-btn>
          <v-btn color="red darken-1" variant="text" @click="deleteItemConfirm" :loading="deleting">削除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { markerApi, uploadApi } from '../services/api'
import type { MarkerMaster } from '../types'

const form = ref()

const markers = ref<MarkerMaster[]>([])
const loading = ref(false)

const markersWithImageUrls = computed(() => {
  return markers.value.map(marker => ({
    ...marker,
    imageUrl: marker.filePath ? getImageUrl(marker.filePath) : null
  }))
})
const dialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editedIndex = ref(-1)
const selectedFile = ref<File[]>([])
const valid = ref(false)

const defaultItem: Partial<MarkerMaster> = {
  name: '',
  filePath: '',
  category: 'OTHER',
  isVisible: true,
  displayOrder: 0,
  memo: '',
  description: '',
  functionType: '',
  paramJson: '',
  isUnlocked: false,
  searchKeyword: '',
  published_at: undefined
}

const editedItem = ref<Partial<MarkerMaster>>({ ...defaultItem })

const categoryOptions = [
  { title: '登録', value: 'REGISTER' },
  { title: '検索', value: 'SEARCH' },
  { title: '機能', value: 'FUNCTION' },
  { title: 'その他', value: 'OTHER' }
]

const headers = [
  { title: 'ID', key: 'id' },
  { title: '名前', key: 'name' },
  { title: '画像', key: 'filePath', sortable: false, width: '80px' },
  { title: 'カテゴリ', key: 'category' },
  // { title: '表示', key: 'isVisible' },
  { title: '配信日', key: 'published_at' },
  { title: '説明', key: 'description' },
  { title: 'アクション', key: 'actions', sortable: false }
]

const formatDate = (timestamp: number | undefined) => {
  if (!timestamp) return '-';
  const date = new Date(timestamp);
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  const hh = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  return `${yyyy}/${mm}/${dd} ${hh}:${min}`;
};

const fetchMarkers = async () => {
  loading.value = true
  try {
    const response = await markerApi.getAll()
    markers.value = response.data
  } catch (error) {
    console.error('Failed to fetch markers:', error)
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  editedIndex.value = -1
  editedItem.value = { ...defaultItem }
  selectedFile.value = []
  dialog.value = true
}

const editItem = (item: MarkerMaster) => {
  editedIndex.value = markers.value.indexOf(item)
  editedItem.value = { ...item }
  selectedFile.value = []
  dialog.value = true
}

const deleteItem = (item: MarkerMaster) => {
  editedIndex.value = markers.value.indexOf(item)
  editedItem.value = { ...item }
  deleteDialog.value = true
}

const close = () => {
  dialog.value = false
  setTimeout(() => {
    editedItem.value = { ...defaultItem }
    editedIndex.value = -1
    selectedFile.value = []
  }, 300)
}

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target && target.files && target.files.length > 0) {
    selectedFile.value = Array.from(target.files)
  } else {
    selectedFile.value = []
  }
}

const save = async () => {
  if (!editedItem.value.name || !editedItem.value.name.trim()) {
    console.error('Validation failed: Name is required');
    return;
  }
  
  if (!editedItem.value.category) {
    console.error('Validation failed: Category is required');
    return;
  }
  
  if (!editedItem.value.description || !editedItem.value.description.trim()) {
    console.error('Validation failed: Description is required');
    return;
  }


  saving.value = true
  try {
    let filePath = editedItem.value.filePath || ''
    
    if (selectedFile.value && selectedFile.value.length > 0) {
      const uploadResponse = await uploadApi.uploadFile(selectedFile.value[0])
      filePath = uploadResponse.data.filePath
    }

    const publishedAtTimestamp = editedItem.value.published_at
      ? (typeof editedItem.value.published_at === 'string'
        ? new Date(editedItem.value.published_at).getTime()
        : editedItem.value.published_at)
      : Date.now();

    const markerData = {
      ...editedItem.value,
      filePath,
      published_at: publishedAtTimestamp || Date.now()
    }

    if (editedIndex.value > -1) {
      await markerApi.update(editedItem.value.id!, markerData)
    } else {
      await markerApi.create(markerData)
    }

    await fetchMarkers()
    close()
  } catch (error) {
    console.error('Failed to save marker:', error)
  } finally {
    saving.value = false
  }
}

const deleteItemConfirm = async () => {
  deleting.value = true
  try {
    await markerApi.delete(editedItem.value.id!)
    await fetchMarkers()
    deleteDialog.value = false
  } catch (error) {
    console.error('Failed to delete marker:', error)
  } finally {
    deleting.value = false
  }
}

const getImageUrl = (filePath: string) => {
  if (filePath.startsWith('http')) {
    return filePath
  }
  return `http://localhost:8000${filePath}`
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  console.error('Image failed to load:', img.src)
}

const handleImageLoad = (event: Event) => {
  const img = event.target as HTMLImageElement
  console.log('Image loaded successfully:', img.src)
}

onMounted(() => {
  fetchMarkers()
})
</script>
