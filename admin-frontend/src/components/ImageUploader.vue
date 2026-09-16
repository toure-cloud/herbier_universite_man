<template>
  <div class="image-uploader">
    <label v-if="label" class="uploader-label">
      <i :class="icon || 'fas fa-image'"></i> {{ label }}
      <span v-if="required" class="required">*</span>
    </label>

    <!-- Zone de dépôt / sélection -->
    <div
      class="drop-zone"
      :class="{ 'has-files': hasFiles, 'is-multiple': multiple }"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      @click="openFileDialog"
    >
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        :multiple="multiple"
        style="display: none"
        @change="handleFileSelect"
      />

      <div class="drop-content">
        <i class="fas fa-cloud-upload-alt"></i>
        <p class="drop-title">
          {{ multiple ? 'Cliquez ou déposez vos images ici' : 'Cliquez ou déposez une image ici' }}
        </p>
        <p class="drop-hint">
          Formats acceptés : {{ acceptList }} • Max {{ maxSize }} Mo
          {{ multiple ? ` • Jusqu'à ${maxFiles} images` : '' }}
        </p>
      </div>
    </div>

    <!-- Prévisualisation -->
    <div v-if="hasFiles" class="preview-grid" :class="{ single: !multiple }">
      <div
        v-for="(preview, index) in previews"
        :key="preview.id || index"
        class="preview-item"
      >
        <img :src="preview.url" :alt="`Aperçu ${index + 1}`" />
        <button
          type="button"
          class="preview-remove"
          @click.stop="removePreview(index)"
          aria-label="Supprimer"
        >
          <i class="fas fa-times"></i>
        </button>
        <span v-if="multiple && previews.length > 1" class="preview-index">
          {{ index + 1 }}
        </span>
      </div>
    </div>

    <p v-if="error" class="uploader-error">
      <i class="fas fa-exclamation-circle"></i> {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelValue: { type: [String, Array, File, Object], default: null },
  label: { type: String, default: '' },
  icon: { type: String, default: '' },
  required: { type: Boolean, default: false },
  multiple: { type: Boolean, default: false },
  accept: { type: String, default: 'image/jpeg,image/png,image/webp,image/gif,image/svg+xml' },
  maxSize: { type: Number, default: 5 },  // Mo
  maxFiles: { type: Number, default: 10 },
});

const emit = defineEmits(['update:modelValue', 'files-changed']);

const fileInput = ref(null);
const isDragging = ref(false);
const error = ref('');
const previews = ref([]);
const files = ref([]);  // Files sélectionnés (pour envoi multipart)

const acceptList = computed(() =>
  props.accept.split(',').map((t) => t.split('/')[1]).join(', ').toUpperCase()
);

const hasFiles = computed(() => previews.value.length > 0);

// ---------- Initialisation depuis modelValue ----------
const initFromModel = (value) => {
  previews.value = [];
  files.value = [];

  if (!value) return;

  const urls = Array.isArray(value) ? value : [value];
  urls.forEach((url, i) => {
    if (typeof url === 'string' && url) {
      previews.value.push({ id: `existing-${i}`, url, existing: true });
    }
  });
};

watch(
  () => props.modelValue,
  (val) => {
    // Ne pas réinitialiser si c'est nous qui avons mis à jour (évite la boucle)
    if (files.value.length === 0) initFromModel(val);
  },
  { immediate: true }
);

// ---------- Handlers ----------
const openFileDialog = () => fileInput.value?.click();

const validateFile = (file) => {
  const allowed = props.accept.split(',').map((s) => s.trim());
  if (!allowed.includes(file.type)) {
    return `Format non supporté : ${file.type}`;
  }
  if (file.size > props.maxSize * 1024 * 1024) {
    return `Fichier trop volumineux (${(file.size / 1024 / 1024).toFixed(1)} Mo)`;
  }
  return null;
};

const addFiles = (fileList) => {
  error.value = '';
  const newFiles = Array.from(fileList);

  if (!props.multiple && newFiles.length > 1) {
    error.value = 'Une seule image autorisée.';
    return;
  }

  const total = previews.value.length + newFiles.length;
  if (props.multiple && total > props.maxFiles) {
    error.value = `Maximum ${props.maxFiles} images autorisées.`;
    return;
  }

  for (const file of newFiles) {
    const err = validateFile(file);
    if (err) { error.value = err; continue; }

    files.value.push(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      previews.value.push({
        id: `new-${Date.now()}-${Math.random()}`,
        url: e.target.result,
        existing: false,
        file,
      });
      emitUpdate();
    };
    reader.readAsDataURL(file);
  }
};

const handleFileSelect = (e) => {
  if (e.target.files?.length) addFiles(e.target.files);
  e.target.value = '';
};

const handleDrop = (e) => {
  isDragging.value = false;
  if (e.dataTransfer.files?.length) addFiles(e.dataTransfer.files);
};

const removePreview = (index) => {
  const preview = previews.value[index];
  if (!preview) return;

  if (!preview.existing) {
    const fileIdx = files.value.findIndex((f) => f === preview.file);
    if (fileIdx !== -1) files.value.splice(fileIdx, 1);
  }

  previews.value.splice(index, 1);
  emitUpdate();
};

// ---------- Émission ----------
const emitUpdate = () => {
  const existingUrls = previews.value.filter((p) => p.existing).map((p) => p.url);
  const hasNewFiles = files.value.length > 0;

  // Si on a de nouveaux fichiers, on expose les Files
  if (hasNewFiles) {
    const value = props.multiple ? files.value : files.value[0];
    emit('update:modelValue', value);
    emit('files-changed', { files: files.value, existing: existingUrls });
  } else {
    // Sinon, on expose juste les URLs existantes
    const value = props.multiple ? existingUrls : existingUrls[0] || null;
    emit('update:modelValue', value);
    emit('files-changed', { files: [], existing: existingUrls });
  }
};

defineExpose({
  getFiles: () => files.value,
  getExisting: () => previews.value.filter((p) => p.existing).map((p) => p.url),
  reset: () => { previews.value = []; files.value = []; },
});
</script>

<style scoped>
.image-uploader { display: flex; flex-direction: column; gap: 8px; }

.uploader-label {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 6px;
}
.uploader-label i { color: #10b981; }
.required { color: #ef4444; }

.drop-zone {
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 28px 20px;
  text-align: center;
  cursor: pointer;
  background: #f8fafc;
  transition: all 0.2s;
}
.drop-zone:hover,
.drop-zone.is-multiple:hover {
  border-color: #10b981;
  background: #ecfdf5;
}
.drop-zone.has-files { padding: 16px; }

.drop-content { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.drop-content i { font-size: 32px; color: #10b981; }
.drop-title { font-size: 14px; font-weight: 600; color: #334155; margin: 0; }
.drop-hint { font-size: 11.5px; color: #94a3b8; margin: 0; }

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 10px;
  margin-top: 10px;
}
.preview-grid.single { grid-template-columns: minmax(120px, 180px); }

.preview-item {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  background: #f1f5f9;
  aspect-ratio: 1 / 1;
  border: 1px solid #e2e8f0;
}
.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.preview-remove {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.9);
  color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: background 0.15s;
}
.preview-remove:hover { background: #dc2626; }

.preview-index {
  position: absolute;
  bottom: 6px;
  left: 6px;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 10px;
}

.uploader-error {
  color: #dc2626;
  font-size: 12px;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>